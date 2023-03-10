C2 = [    
	{ 
			"Title": "EXFILTRATION OVER PHYSICAL MEDIUM",            
			"description": "The attackers use a USB drive, printouts, or even socks... yes, socks, as a way to get data out of a network. This requires an accomplice on the inside or it can be used with the Insider Threat (Initial Compromise) card.",            "detection": ["Physical Security Review", "Endpoint Security Protection Analysis", "Endpoint Analysis", "User Awareness Training"],
            "tools": ["USB drive/socks and a dream... a dream of evil."],
            "documentation": "https://attack.mitre.org/techniques/T1052"
    },
    {
            "Title": "GMAIL, TUMBLR, SALESFORCE, TWITTER AS C2",
            "description": "The attackers route traffic through third-party services. Many services, like Gmail, are ignored completely by many security tools.",
            "detection": ["NetFlow", "Zeek/Bro", "RITA Analysis"],
            "tools": ["Gcat", "Sneak Creeper"],
            "documentation": ["https://github.com/byt3b|33d3r/gcat", "https://github.com/DakotaNelson/sneaky-creeper"]
    },
    {
            "Title": "WINDOWS BACKGROUND INTELLIGENT TRANSFER SERVICE (BITS)",
            "description": "The attackers use BITS, another protocol that is often ignored.",
            "detection": ["NetFlow", "Zeek/Bro", "RITA Analysis"],
            "documentation": "https://www.blackhillsinfosec.com/bypassing-cylance-part-2-using-dnscat2"
    },
    {
            "Title": "DNS AS C2",
            "description": "The attackers use DNS as a C2 channel.",
            "detection": ["NetFlow", "Zeek/Bro", "RITA Analysis"],
            "tools": ["dnscat2"],
            "documentation": "https://github.com/deruke/tools"
    },
    {
            "Title": "DOMAIN FRONTING AS C2",
            "description": "The attackers use Domain Fronting to bounce their traffic off of legitimate systems.",
            "detection": ["NetFlow", "Zeek/Bro", "RITA Analysis"],
            "tools": ["Cobalt Strike"],
            "documentation": ["https://www.cobaltstrike.com", "https://www.blackhillsinfosec.com/bypass-web-proxy-filtering"]
    },
    {
            "Title": "HTTP AS EXFIL",
            "description": "The attackers use HTTP as an exfil method. This is usually used in conjunction with some type of stego. For example, VSAgent uses base64 encoded __ VIEWSTATE as an exfil field.",
            "detection": ["NetFlow", "Zeek/Bro", "RITA Analysis"],
            "tools": ["Metasploit Reverse HTTP Payloads", "VSAgent", "Prismatica"],
            "documentation": ["https://www.blackhillsinfosec.com/504-vsagent-usage-instructions", "https://github.com/Project-Prismatica/Prismatica"]
    }
]
