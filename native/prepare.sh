#!/usr/bin/env bash
# Prepares the Capacitor native project for one platform: bash native/prepare.sh android|ios
set -euo pipefail
P="$1"
if [ "$P" = android ]; then DIR=native-android; else DIR=native-ios; fi
npm install --no-audit --no-fund
rm -rf www && mkdir -p www
cp -r index.html manifest.webmanifest icons skin www/
python3 -m pip install --quiet pillow 2>/dev/null || python3 -m pip install --quiet --break-system-packages pillow
python3 native/assets.py
[ -d "$DIR" ] || npx cap add "$P"
if [ "$P" = android ]; then
  npx capacitor-assets generate --android --androidProject "$DIR" --iconBackgroundColor '#9fb6ff' --splashBackgroundColor '#9fb6ff'
else
  npx capacitor-assets generate --ios --iosProject "$DIR/App" --iconBackgroundColor '#9fb6ff' --splashBackgroundColor '#9fb6ff'
fi
npx cap sync "$P"
VC="${GITHUB_RUN_NUMBER:-1}"
if [ "$P" = android ]; then
  M="$DIR/app/src/main/AndroidManifest.xml"
  grep -q screenOrientation "$M" || sed -i 's/<activity/<activity android:screenOrientation="portrait"/' "$M"
  G="$DIR/app/build.gradle"
  sed -i -E "s/versionCode [0-9]+/versionCode $VC/; s/versionName \"[^\"]*\"/versionName \"1.0.$VC\"/" "$G"
  grep -E "versionCode|versionName|targetSdk|compileSdk" "$G" "$DIR/variables.gradle" || true
else
  PL="$DIR/App/App/Info.plist"
  /usr/libexec/PlistBuddy -c "Delete :UISupportedInterfaceOrientations" "$PL" || true
  /usr/libexec/PlistBuddy -c "Add :UISupportedInterfaceOrientations array" -c "Add :UISupportedInterfaceOrientations:0 string UIInterfaceOrientationPortrait" "$PL"
  /usr/libexec/PlistBuddy -c "Delete :UISupportedInterfaceOrientations~ipad" "$PL" || true
  /usr/libexec/PlistBuddy -c "Set :UIRequiresFullScreen true" "$PL" 2>/dev/null || /usr/libexec/PlistBuddy -c "Add :UIRequiresFullScreen bool true" "$PL"
  /usr/libexec/PlistBuddy -c "Set :ITSAppUsesNonExemptEncryption false" "$PL" 2>/dev/null || /usr/libexec/PlistBuddy -c "Add :ITSAppUsesNonExemptEncryption bool false" "$PL"
  PB="$DIR/App/App.xcodeproj/project.pbxproj"
  sed -i '' -E 's/TARGETED_DEVICE_FAMILY = "1,2";/TARGETED_DEVICE_FAMILY = 1;/g; s/CURRENT_PROJECT_VERSION = [0-9]+;/CURRENT_PROJECT_VERSION = '"$VC"';/g; s/MARKETING_VERSION = [0-9.]+;/MARKETING_VERSION = 1.0;/g' "$PB"
  grep -E "TARGETED_DEVICE_FAMILY|IPHONEOS_DEPLOYMENT_TARGET|CURRENT_PROJECT_VERSION" "$PB" | sort -u || true
fi
echo "prepared $P in $DIR"
