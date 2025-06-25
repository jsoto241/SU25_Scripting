
--Jose Soto

math.randomseed(os.time()) -- Seed random number generator
--variables for use in code
local secretNumber
local maxAttempts = 7
local attemptCount
local userGuess
local guessedCorrectly
local userResponse = "yes"

--Code that begins the game loop

while userResponse == "yes" do
    secretNumber = math.random(1, 100)
    attemptCount = 0
    guessedCorrectly = false

    --Prompt user to guess a number
    print("Guess the number between 1 and 100. You have 7 attempts.")

    --Check to see if player has attempts for their guess
    while attemptCount < maxAttempts and not guessedCorrectly do
        io.write("Enter your guess: ")
        userGuess = tonumber(io.read())
        attemptCount = attemptCount + 1

        --Check if number is guessed correctly, and prvide hint if not
        if userGuess == secretNumber then
            guessedCorrectly = true
            print("You guessed correctly in " .. attemptCount .. " attempt(s)!")
        elseif userGuess < secretNumber then
            print("Too low!")
        else
            print("Too high!")
        end
    end

    --Fail state for user
    if not guessedCorrectly then
        print("You lost! The number was " .. secretNumber)
    end
    --Prompt to continue game or end game
    io.write("Play again? (yes/no): ")
    userResponse = io.read()
end

print("Thanks for playing! Goodbye.")
