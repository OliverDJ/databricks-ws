module Producer

open Service
open Models
open System.Threading.Tasks
open Microsoft.Azure.WebJobs
open Microsoft.Extensions.Logging
open FSharp.Control.Tasks.V2.ContextInsensitive

let tee f x =
    f x
    x

[<FunctionName("UserProducer")>]
let run (
        [<TimerTrigger("0,20,40 * * * * *")>] timer: TimerInfo, 
        [<EventHub(eventHubName = "",
            Connection = "eventhubwriter")>] eventhub: IAsyncCollector<EventhubMessage<User>>,
        log: ILogger) =
        task {
            let allSSn = Samples.getSsns()
            let maleNames = Samples.getMaleNames()
            let femaleNames = Samples.getFemaleNames()
            let lastNames = Samples.getLastNames()

            let addToEH = eventhub.AddAsync

            let maleSsn = allSSn |> getMaleSsns
            let femaleSsn = allSSn |> getFemaleSsns

            let rnd = System.Random()
            
            let _createUser = 
                createGenderSpecificUser 
                    rnd lastNames maleSsn maleNames femaleSsn femaleNames

            let nrOfUsers = 100

            let print x =  x |> sprintf "sending %A" |> log.LogInformation

            let! u = 
                nrOfUsers
                |> pickMaleAndFemales rnd  // [0,1,1,0,1,0]
                |> List.map(_createUser) 
                |> List.map (EventhubMessage.Create "1.0.1")
                |> List.map(tee print)
                |> List.map(addToEH) 
                |> Task.WhenAll 

            return ()
        }
        