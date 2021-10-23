module Service
open Models

let (|Male | Female|) input = 
    if input % 2 = 0 then Female else Male
   
let private _isGender t (x: string) =
    let c = x.[8] |> string |> int 
    (%) c 2 = t


let pickMaleAndFemales (rnd: System.Random)  count =
    List.init count (fun _ -> rnd.Next(0,2))

let getrandomitem (rnd: System.Random) (li: string list) =  
  li.[rnd.Next(li.Length)]

let createRandomUser rnd lastName ssns names =
    let ssn = ssns |> getrandomitem rnd
    let name = names |> getrandomitem rnd
    let lastName = lastName |> getrandomitem rnd
    (name, ssn, lastName) |||> User.Create 


let createGenderSpecificUser rnd ln ms mn fs fn n = 
    match n with 
    | Male -> (ms, mn) ||> createRandomUser rnd ln
    | Female -> (fs, fn) ||> createRandomUser rnd ln

let getMaleSsns ssn = 
    ssn
    |> List.filter(_isGender 1)

let getFemaleSsns ssn = 
    ssn
    |> List.filter(_isGender 0)


