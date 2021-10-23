module test =

    let ssn = [
        "27128549841"
        "01017849871"
        "05040422651"
        "11128949668"
        "02037949488"
        "01021099879"
        "01017949973"
        "01017849952"
        "01017849952"
        "01016849924"
        "01014449813"
        "01014349983"
        "01011549779"
        "01029249993"
        "01029349823"
    ]

    let maleNames = [
        "Liam"
        "Noah"
        "Elijah"
        "William"
        "James"
        "Benjamin"
        "Oliver"
        "Lucas"
        "Henry"
        "Alexander"
        "Mason"
        "Michael"
        "Ethan"
        "Daniel"
        "Jacob"
        "Logan"
        "Jackson"
        "Levi"
        "Sebastian"
        "Mateo"
        "Jack"
        "Owen"
        "Theodore"
        "Aiden"
        "Samuel"
    ]

    let femaleNames =
        [
            "Olivia"
            "Emma"
            "Ava"
            "Charlotte"
            "Sophia"
            "Amelia"
            "Isabella"
            "Mia"
            "Evelyn"
            "Harper"
            "Camila"
            "Gianna"
            "Abigail"
            "Luna"
            "Ella"
            "Elizabeth"
            "Sofia"
            "Emily"
            "Avery"
            "Mila"
            "Scarlett"
            "Eleanor"
            "Madison"
            "Layla"
            "Penelope"
        ]

    let lastNames =
        [
            "Smith"
            "Johnson"
            "Williams"
            "Brown"
            "Jones"
            "Garcia"
            "Miller"
            "Davis"
            "Rodriguez"
            "Martinez"
            "Hernandez"
            "Lopez"
            "Gonzalez"
            "Wilson"
            "Anderson"
            "Taylor"
            "Moore"
            "Jackson"
            "Martin"
            "Lee"
            "Perez"
            "Thompson"
            "White"
            "Li"
        ]

    let (|Male | Female|) input = 
        if input % 2 = 0 then Female else Male
   
    let isGender t (x: string) =
        let c = x.[8] |> string |> int 
        (%) c 2 = t
    
    type User = 
        {
            Name: string
            Ssn: string
            LastName: string
        } with static member Create n ssn ln =
                { Name = n; Ssn = ssn; LastName = ln}

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

    let maleSsn = 
        ssn
        |> List.filter(isGender 1)

    let femaleSsn = 
        ssn
        |> List.filter(isGender 0)

    let rnd = System.Random()

    let _createUser = 
        createGenderSpecificUser 
            rnd lastNames maleSsn maleNames femaleSsn femaleNames

    let r = 
        10
        |> pickMaleAndFemales rnd
        |> List.toArray
        |> Array.map (_createUser)