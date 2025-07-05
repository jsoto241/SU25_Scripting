--REMEMBER WITH OUR DEBUGGER F5 for debug, SHIFT F5 for non-debug 
if arg[2] == "debug" then
    require("lldebugger").start()
end

-- Load images and title
function titleLoad()
    narwhalImage = love.graphics.newImage("narwhal.png")
    titleText = "Narwhal Drop"
    love.window.setTitle(titleText)
end

function love.load()
    success = love.window.updateMode(1024, 768)
    titleLoad()

    scene = 1 -- 0 = title, 1 = game, 2 = game over

    -- Narwhal (was slime) variables
    narwhalNums = 5
    narwhalX, narwhalY, narwhalSpeed = {}, {}, {}
    minSpeed = 10
    maxSpeed = 20
    speedMod = 1
    narwhalCount = narwhalNums

    -- Power-up variables
    powerup = nil
    powerupSpawnTimer = 0
    powerupSpawnInterval = 20
    powerupActive = false
    powerupTimer = 0
    powerupDuration = 5

    -- Random seed
    math.randomseed(os.time())
    math.random(); math.random(); math.random()

    -- Create narwhals
    while narwhalCount > 0 do
        narwhalX[#narwhalX + 1] = math.random(0, love.graphics.getWidth() - narwhalImage:getWidth())
        narwhalY[#narwhalY + 1] = 0
        narwhalSpeed[#narwhalSpeed + 1] = math.random(minSpeed, maxSpeed)
        narwhalCount = narwhalCount - 1
    end
end

function love.mousepressed(x, y, button, istouch)
    if button == 1 then
        if scene == 0 then
            -- Future: start game from title
        elseif scene == 1 then
            -- Check narwhals
            for i = #narwhalX, 1, -1 do
                if x >= narwhalX[i] and x <= narwhalX[i] + narwhalImage:getWidth() and
                   y >= narwhalY[i] and y <= narwhalY[i] + narwhalImage:getHeight() then

                    speedMod = speedMod + 1
                    maxSpeed = maxSpeed + speedMod

                    narwhalX[i] = math.random(0, love.graphics.getWidth() - narwhalImage:getWidth())
                    narwhalY[i] = -math.random(narwhalImage:getHeight(), narwhalImage:getHeight() * 2)
                    narwhalSpeed[i] = math.random(minSpeed, maxSpeed)
                    break
                end
            end

            -- Check power-up
            if powerup and x >= powerup.x and x <= powerup.x + narwhalImage:getWidth() and
                         y >= powerup.y and y <= powerup.y + narwhalImage:getHeight() then
                powerupActive = true
                powerup = nil
                powerupTimer = 0
            end
        end
    end
end

function love.update(dt)
    if scene == 1 then
        -- Update narwhals
        for i, _ in ipairs(narwhalX) do
            local speed = powerupActive and narwhalSpeed[i] * 0.5 or narwhalSpeed[i]
            narwhalY[i] = narwhalY[i] + speed * dt

            if narwhalY[i] + narwhalImage:getHeight() >= love.graphics.getHeight() then
                scene = 2 -- game over
            end
        end

        -- Spawn power-up
        powerupSpawnTimer = powerupSpawnTimer + dt
        if powerupSpawnTimer >= powerupSpawnInterval and not powerup then
            powerup = {
                x = math.random(0, love.graphics.getWidth() - narwhalImage:getWidth()),
                y = math.random(0, love.graphics.getHeight() - narwhalImage:getHeight())
            }
            powerupSpawnTimer = 0
        end

        -- Power-up timer
        if powerupActive then
            powerupTimer = powerupTimer + dt
            if powerupTimer >= powerupDuration then
                powerupActive = false
                powerupTimer = 0
            end
        end
    end
end

function love.draw()
    if scene == 0 then
        -- Draw title screen (future use)
        love.graphics.printf("Narwhal Drop\nClick to Start", 0, 300, 1024, "center")
    elseif scene == 1 then
        -- Draw narwhals
        for i, _ in ipairs(narwhalX) do
            love.graphics.draw(narwhalImage, narwhalX[i], narwhalY[i])
        end

        -- Draw power-up (green tint)
        if powerup then
            love.graphics.setColor(0, 1, 0)
            love.graphics.draw(narwhalImage, powerup.x, powerup.y)
            love.graphics.setColor(1, 1, 1)
        end

        -- UI
        love.graphics.print("Power-Up Active: " .. tostring(powerupActive), 10, 10)
    elseif scene == 2 then
        love.graphics.printf("Game Over!\nPress ESC to quit", 0, 300, 1024, "center")
    end
end

-- Error debugger
local love_errorhandler = love.errorhandler
function love.errorhandler(msg)
    if lldebugger then
        error(msg, 2)
    else
        return love_errorhandler(msg)
    end
end
