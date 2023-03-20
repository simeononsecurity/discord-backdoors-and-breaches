pivot_and_escalate = [
    {
        "Title": "INTERNAL PASSWORD SPRAY",
        "Description": "The attackers start a password spray against the rest of the organization from a compromised system.",
        "Detection": ["User and Entity Behavior Analytics", "SIEM Log Analysis"],
        "tools": ["Domain Password Spray"],
        "documentation": [
            "https://github.com/dafthack/DomainPasswordSpray",
            "https://www.blackhillsinfosec.com/webcast-attack-tactics-5-zero-to-hero-attack",
        ],
    },
    {
        "Title": "KERBEROASTING",
        "Description": "The attackers use a feature of SPNs to extract and crack service passwords.",
        "Detection": [
            "SIEM Log Analysis",
            "User and Entity Behavior Analytics",
            "Honey Services",
            "Internal Segmentation",
        ],
        "tools": ["GetUserSPNs.py from Impacket", "Hashcat for Cracking"],
        "documentation": [
            "https://www.blackhillsinfosec.com/running-hashcat-on-ubuntu-18-04-server-with-1080ti",
            "https://github.com/SecureAuthCorp/impacket/blob/master/examples/GetUserSPNs.py",
        ],
    },
    {
        "Title": "WEAPONIZING ACTIVE DIRECTORY",
        "Description": "The attackers map trust relationships and user/group privileges in your Active Directory Network.",
        "Detection": [
            "SIEM Log Analysis",
            "User and Entity Behavior Analytics",
            "Internal Segmentation",
        ],
        "tools": ["BloodHound", "Death Star", "CrackMapExec"],
        "documentation": [
            "https://github.com/BloodHoundAD/BloodHound",
            "https://github.com/byt3bl33d3r/DeathStar",
            "https://github.com/byt3bl33d3r/CrackMapExec",
            "https://www.blackhillsinfosec.com/webcast-weaponizing-active-directory",
        ],
    },
    {
        "Title": "CREDENTIAL STUFFING",
        "Description": "Valid Active Directory credentials have been discovered on open shares and files within your environment. These are used by the attackers.",
        "Detection": [
            "SIEM Log Analysis",
            "User and Entity Behavior Analytics",
            "Internal Segmentation",
        ],
        "tools": [
            "ADExplorer.exe",
            "Invoke-ShareFinder",
            "Invoke-FileFinder",
            "Find-InterestingFile",
            "MailSniper",
        ],
        "documentation": [
            "https://www.blackhillsinfosec.com/domain-goodness-learned-love-ad-explorer",
            "https://www.blackhillsinfosec.com/abusing-exchange-mailbox-permissions-mailsniper",
        ],
    },
    {
        "Title": "NEW SERVICE CREATION",
        "Description": "The attackers create and load their malware using a service with SYSTEM privileges. Or, they just create a new service.",
        "Detection": ["Endpoint Analysis", "Endpoint Security Protection Analysis"],
        "tools": ["Metasploit getsystem and other Post-Exploitation Scripts"],
        "documentation": "https://www.metasploit.com",
    },
    {
        "Title": "LOCAL PRIVILEGE ESCALATION",
        "Description": "The attackers use a vulnerability in local software to gain administrative access.",
        "Detection": ["Endpoint Analysis", "Endpoint Security Protection Analysis"],
        "tools": ["PowerSploit's PowerUp", "Meterpreter Post-Exploitation Scripts"],
        "documentation": "https://www.blackhillsinfosec.com/powershell-without-powershell-how-to-bypass-application-whitelisting-environment-restrictions-av",
    },
    {
        "Title": "BROADCAST/MULTICAST PROTOCOL POISONING",
        "Description": "For years, LANMAN was the worst thing in Windows. Then LLMNR said Stand Back and Hold My Beer! Basically, LLMNR lets a host ask for name resolution from any system on the same network. The attackers perform Broadcast/Multicast protocol poisoning on your Active Directory Network.",
        "Detection": [
            "CredDefense Toolkit",
            "User and Entity Behavior Analytics",
            "Firewall Log Review",
        ],
        "tools": ["Responder attacks LLMNR", "NBI-NS", "and mDNS."],
        "documentation": [
            "https://github.com/Igandx/Responder",
            "https://www.blackhillsinfosec.com/how-to-disable-Ilmnr-why-you-want-to",
        ],
    },
]
