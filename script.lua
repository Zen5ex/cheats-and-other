local function cheatapi()
g_Config:FindVar("Aimbot","AntiAim","Fake Lag","Limit"):SetInt(4)
end

cheat.RegisterCallback("createmove", cheatapi)
