module Producer

open System
open System.IO
open Microsoft.AspNetCore.Mvc
open Microsoft.Azure.WebJobs
open Microsoft.Azure.WebJobs.Extensions.Http
open Microsoft.AspNetCore.Http
open Newtonsoft.Json
open Microsoft.Extensions.Logging
open Microsoft.Azure.EventHubs
open Samples
open FSharp.Control.Tasks.V2.ContextInsensitive
open Service
open System.Threading.Tasks
open Models


let tee f x =
    f x
    x

[<FunctionName("GetUserSamples")>]
let run (
        //[<HttpTrigger(AuthorizationLevel.Function, "get", Route = "usersample" )>]req: HttpRequest, 
        [<TimerTrigger("%crontab%")>] timer: TimerInfo, 
        [<EventHub(eventHubName = "databricks-workshop",
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

            let nrOfUsers = 10

            let messages = 
                nrOfUsers
                |> pickMaleAndFemales rnd  // [0,1,1,0,1,0]
                |> List.map(_createUser) // Users
                |> List.map (EventhubMessage.Create "1.0.1")

            let! u = 
                messages 
                |> List.map(tee(printfn "sending %A") )
                |> List.map(addToEH) 
                |> Task.WhenAll 

            //return OkObjectResult(messages) :> IActionResult
            return ()
        }
        