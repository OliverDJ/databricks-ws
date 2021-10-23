module Model

[<CLIMutable>]
type AppSettings = 
    {
        eventhubreader: string
        eventhubwriter: string

    }