[Setup]
AppName=ScreenMonitorApp
AppVersion=1.1.0
DefaultDirName={pf}\ScreenMonitorApp
DefaultGroupName=ScreenMonitorApp
PrivilegesRequired=admin 
AllowNoIcons=yes
OutputDir=output
OutputBaseFilename=ScreenMonitorAppInstaller
Compression=lzma
SolidCompression=yes

[Files]
; Copia tutti i file generati da PyInstaller
Source: "dist\ScreenMonitorApp\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; Assicurati di includere l'icona
Source: "icon.ico"; DestDir: "{app}"

[UninstallDelete]
; Elimina il file settings.ini da AppData durante la disinstallazione
Type: files; Name: "{userappdata}\ScreenMonitorApp\settings.ini"

; Elimina la directory ScreenMonitorApp in AppData (solo se vuota)
Type: dirifempty; Name: "{userappdata}\ScreenMonitorApp"

; Elimina la directory ScreenMonitorApp in Program Files (solo se vuota)
Type: dirifempty; Name: "{app}\ScreenMonitorApp"

[Icons]
Name: "{group}\ScreenMonitorApp"; Filename: "{app}\ScreenMonitorApp.exe"; IconFilename: "{app}\icon.ico"
Name: "{userdesktop}\ScreenMonitorApp"; Filename: "{app}\ScreenMonitorApp.exe"; IconFilename: "{app}\icon.ico"


;[INI]
; Crea il file settings.ini se non esiste
;Filename: "{app}\settings.ini"; Section: "Settings"; Key: "monitor_index"; String: "0"
;Filename: "{app}\settings.ini"; Section: "Settings"; Key: "sensitivity"; String: "500000"
;Filename: "{app}\settings.ini"; Section: "Settings"; Key: "tabs_to_navigate"; String: "0"
;Filename: "{app}\settings.ini"; Section: "Settings"; Key: "rights_to_navigate"; String: "1"

[Run]
Filename: "{app}\ScreenMonitorApp.exe"; Description: "Avvia ScreenMonitorApp"; Flags: nowait postinstall skipifsilent

