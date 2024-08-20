[Setup]
AppName=ScreenMonitorApp
AppVersion=1.1.1
DefaultDirName={pf}\ScreenMonitorApp
DefaultGroupName=ScreenMonitorApp
PrivilegesRequired=admin  
AllowNoIcons=yes
OutputDir=output
OutputBaseFilename=ScreenMonitorAppInstaller
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\ScreenMonitorApp\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\ScreenMonitorApp"; Filename: "{app}\ScreenMonitorApp.exe"; IconFilename: "{app}\icon.ico"

[Run]
Filename: "{app}\ScreenMonitorApp.exe"; Description: "Avvia ScreenMonitorApp"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Elimina la directory ScreenMonitorApp in AppData (solo se vuota)
Type: dirifempty; Name: "{userappdata}\ScreenMonitorApp"

Type: files; Name: "{userappdata}\ScreenMonitorApp\settings.ini"
Type: dirifempty; Name: "{userappdata}\ScreenMonitorApp"

