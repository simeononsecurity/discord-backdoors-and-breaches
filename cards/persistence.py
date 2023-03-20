Persistence = [
    {
        "Title": "MALICIOUS SERVICE/JUST MALWARE",
        "Description": "The attackers add a service that starts every time the system starts.",
        "Detection": ["Endpoint Security Protection Analysis", "Endpoint Analysis"],
        "tools": [
            "Metasploit Persistence",
            "auto runs.exe",
            "msconfig.exe",
            "SILENTTRINITY",
        ],
        "documentation": "https://github.com/byt3b133d3r/SILENTTRINITY",
    },
    {
        "Title": "DLL ATTACKS",
        "Description": "The attackers hijack the order in which DLLs are loaded. This is usually done through insecure directory/file permissions.",
        "Detection": ["Endpoint Security Protection Analysis", "Endpoint Analysis"],
        "tools": ["PowerSploit", "InvisiMole"],
        "documentation": "https://www.blackhillsinfosec.com/digging-deeper-vulnerable-windows-services",
    },
    {
        "Title": "MALICIOUS DRIVER",
        "Description": "The attackers load a malicious driver into the operating system.",
        "Detection": ["Endpoint Security Protection Analysis", "Endpoint Analysis"],
        "tools": ["Pasam", "ROCKBOOT", "Wingbird", "Alureon", "SeaDuke"],
        "documentation": "https://en.wikipedia.org/wiki/Alureon",
    },
    {
        "Title": "ADDING NEW USER",
        "Description": "The attackers add a new user to the local computer.",
        "Detection": ["Endpoint Security Protection Analysis", "Endpoint Analysis"],
        "tools": ["Metasploit", "Cobalt Strike"],
        "documentation": [
            "https://www.metasploit.com",
            "https://www.cobaltstrike.com",
        ],
    },
    {
        "Title": "APPLICATION SHIMMING",
        "Description": "The attackers use the Application Compatibility Toolkit to trick applications into not seeing the ports, directories, files, and services the attackers want to hide.",
        "Detection": ["Endpoint Security Protection Analysis", "Endpoint Analysis"],
        "tools": ["Windows Assessment and Deployment Kit (ADK)"],
        "documentation": [
            "https://docs.microsoft.com/en-us/windows-hardware/get-started/adk-install",
            "https://attack.mitre.org/techniques/T1138",
        ],
    },
    {
        "Title": "MALICIOUS BROWSER PLUGINS",
        "Description": "The attackers install plugins in the browser. This can be used as part of C2 and persistence. The browser is the new endpoint.",
        "Detection": [
            "Endpoint Security Protection Analysis",
            "Endpoint Analysis",
            "Web Proxy (Firewall Log Review)",
            "NetFlow, Zeek/Bro, RITA Analysis",
        ],
        "tools": ["Grammarly is a Keylogger", "graniet/chromebackdoor"],
        "documentation": [
            "https://www.kaspersky.com/blog/browser-extensions-security/20886",
            "https://github.com/graniet/chromebackdoor",
        ],
    },
    {
        "Title": "LOGON SCRIPTS",
        "Description": "The attackers install a script that triggers when a user logs on.",
        "Detection": ["Endpoint Security Protection Analysis", "Endpoint Analysis"],
        "tools": ["Meterpreter Persistence"],
        "documentation": "https://www.metasploit.com",
    },
    {
        "Title": "EVIL FIRMWARE",
        "Description": "The attackers update the firmware of Network Cards, Video Cards, and BIOS or UEFI... with Evil! All of these are very difficult to detect and very difficult to update.",
        "Detection": [
            "Endpoint Security Protection Analysis",
            "Endpoint Analysis",
            "Prayers to an Engaged and Merciful God",
        ],
        "tools": ["Hacking Team UEFI Rootkit", "BadBIOS (... maybe.)"],
        "documentation": "https://threatpost.com/uefi-rootkit-sednit/140420",
    },
    {
        "Title": "ACCESSIBILITY FEATURES",
        "Description": "The attackers hijack Accessibility Features like Sticky Keys and Onscreen Keyboard.",
        "Detection": ["Endpoint Analysis", "Endpoint Security Protection Analysis"],
        "tools": ["Bash Bunny", "USB Rubber Ducky"],
        "documentation": "https://shop.hak5.org",
    },
]
