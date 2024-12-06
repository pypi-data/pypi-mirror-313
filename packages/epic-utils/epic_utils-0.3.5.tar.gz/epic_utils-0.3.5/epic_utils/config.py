class RobloxAPIConfig:
    DATASTOREURL = "https://apis.roblox.com/cloud/v2/universes/{universeid}/data-stores"
    ENTRIESURL = "https://apis.roblox.com/cloud/v2/universes/{universeid}/data-stores/{datastore}/entries"
    ENTRYURL = "https://apis.roblox.com/cloud/v2/universes/{universeid}/data-stores/{datastore}/entries/{entry}"
    ENTRYINCREMENTURL = "https://apis.roblox.com/cloud/v2/universes/{universeid}/data-stores/{datastore}/entries/{entry}:increment"
    UNIVERSEURL = "https://apis.roblox.com/cloud/v2/universes/{universeid}"
    UNIVERSERESTARTURL = "https://apis.roblox.com/cloud/v2/universes/{universeid}:restartServers"
    PAGESIZE = 50