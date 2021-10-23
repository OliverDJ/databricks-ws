

module Models

type EventhubMessage<'T> = 
    {
        Version: string
        Payload: 'T
    } with
    static member Create version (model: 'T) =
        {
            Version = version
            Payload = model
        }

type User = 
    {
        Name: string
        Ssn: string
        LastName: string
    } with static member Create n ssn ln =
            { Name = n; Ssn = ssn; LastName = ln}
