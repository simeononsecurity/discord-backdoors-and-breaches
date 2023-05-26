Procedures = [
    {
        "Title": "SECURITY INFORMATION AND EVENT MANAGEMENT (SIEM) LOG ANALYSIS",
        "Description": "Yeah... good luck with this one. Are you logging the right things? Do you regularly emulate attack scenarios to see if you can detect them?",
        "Tools": "SOF-ELK JPGert Tools Analysis",
        "Documentation": "https://github.com/philhagen/sof-elk https://jpcertcc.github.io/ToolAnalysisResultSheet",
        "Image":"https://i.imgur.com/DrbEhX1.png",
    },
    {
        "Title": "SERVER ANALYSIS",
        "Description": "The ability to baseline a system and verify that it is operating in a normal state. By the way, this is more than simply running Task Manager and looking for eyil_backdoonexe.",
        "Tools": "DeepBlueCLI SANS Analysis Cheat Sheets",
        "Documentation": "https://github.com/sans-blue-team/DeepBlueCLI",
    },
    {
        "Title": "FIREWALL LOG REVIEW",
        "Description": "Can your organization analyze and understand firewall logs? Do you regularly emulate attack scenarios and verify that your procedures work?",
        "Tools": "SOF-ELK",
        "Documentation": "https://github.com/philhagen/sof-elk",
    },
    {
        "Title": "NETFLOW, ZEEK/BRO, REAL INTELLIGENCE THREAT ANALYTICS (RITA) ANALYSIS",
        "Description": "Does your organization capture and review network traffic? Good! Do you know how to parse and review it? Is that process documented? Or, do you just run Zeek/Security Onion/ELK because the cool kids are doing it?",
        "Tools": "Real Intelligence Threat Analytics (RITA) Security Onion AI-Hunter",
        "Documentation": "https://www.activecountermeasures.com/free-tools/rita https://securityonion.net https://www.activecountermeasures.com",
    },
    {
        "Title": "INTERNAL SEGMENTATION",
        "Description": "Turn on your host-based firewalls. Segment different organizational units.Treat the internal network as hostile, because it is.",
        "Tools": "netsh advfirewall Windows Defender Firewall iptables",
        "Documentation": "",
    },
    {
        "Title": "ENDPOINT SECURITY PROTECTION ANALYSIS",
        "Description": "We know, you have AV. Great! Do you actually get alerts and logs? Do you immediately review them? Or, do you simply turn it on and walk away while the network explodes like you're in a bad action movie?",
        "Tools": "LogonTracer",
        "Documentation": "ttps://github.com/JPCERTCC/LogonTracer",
    },
    {
        "Title": "ENDPOINT ANALYSIS",
        "Description": "This is where the defenders use their SANS IR Cheat Sheets to detect attacks on workstations. Time to bring in the Help Desk... and pray.",
        "Tools": "DeepBlueCLI SANS IR Cheat Sheets",
        "Documentation": "https://github.com/sans-blue-team/DeepBlueCLI",
    },
    {
        "Title": "ISOLATION",
        "Description": "Your NetworkTeam is on their game. They can easily isolate infected systems to prevent further harm.",
        "Tools": "Switch and Router Commands",
        "Documentation": "",
    },
    {
        "Title": "CRISIS MANAGEMENT",
        "Description": "Your Legal and ManagementTeams have procedures for effectively and ethically notifying impacted victims of compromises.",
        "Notes": "This counteracts the Data Uploaded to Pastebin Inject Card.",
        "Tools": "This almost never happens. But, a good notification strategy will really help deal with the political fallout.",
        "Documentation": "",
    },
    {
        "Title": "USER AND ENTITY BEHAVIOR ANALYTICS (UEBA)",
        "Description": "It's like logging, but it actually works. UEBA looks for multiple concurrent logins, impossible logins based on geography, unusual file access, passwords sprays, and more!",
        "Tools": "LogonTracer",
        "Documentation": "https://github.com/JPCERTCC/LogonTracer",
    },
]
