-- Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery
select * from crime_scene_reports where day = 28 and month = 7 and description like "%bakery%";

-- Ruth Eugene Raymond
-- the thief withdrawn some money on ATM on Leggett Street
-- He called someone, speaked les than a minute, they are flying next day on the earliest flight
select * from airports;
-- Fiftyville ID is 8
-- earliest flight from Fiftyville is at 08:20
select * from flights where origin_airport_id = 8 and day = 29 order by hour;

-- all passangers that are flown on 08/29 on flight 36
select * from passengers where flight_id = 36;


-- all persons who withdrawn some money on Legget Street on 07/28 will put in list
select * from people
join bank_accounts on people.id = bank_accounts.person_id
where account_number in
    (select account_number from atm_transactions
    where atm_location = "Leggett Street"
    and transaction_type = "withdraw"
    and day = 28
    and month = 7);

-- FIRST LIST OF SUSPECTS
select name from people where passport_number in (select passport_number from passengers where flight_id = 36);

--UPDATED SUSPECT LIST
select * from people
join bank_accounts on people.id = bank_accounts.person_id
where account_number in
    (select account_number from atm_transactions
    where atm_location = "Leggett Street"
    and transaction_type = "withdraw"
    and day = 28
    and month = 7)
    and name in
    (select name from people where passport_number in (select passport_number from passengers where flight_id = 36));


-- Updated list of susspects
select * from people
join bank_accounts on people.id = bank_accounts.person_id
where account_number in
    (select account_number from atm_transactions
    where atm_location = "Leggett Street"
    and transaction_type = "withdraw"
    and day = 28
    and month = 7)
    and name in
    (select name from people where passport_number in (select passport_number from passengers where flight_id = 36))
    and phone_number in (select caller from phone_calls where day = 28 and month = 7 and duration <60);

-- Potential suspects are Bruce and Kenny
select * from bakery_security_logs where license_plate in ("94KL13X","30G67EN","1106N58") and day = 28;
-- It was mentioned that the thief exited after the call ended what makes the exit time to be aproximate to 10:15 only Bruce suits this condition
-- Bruces number (367) 555-5533
-- partners number  (375) 555-8161