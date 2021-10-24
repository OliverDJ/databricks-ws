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




[<FunctionName("GetUserSamples")>]
let run (
        [<HttpTrigger(AuthorizationLevel.Function, "get", Route = "usersample" )>]req: HttpRequest, 
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

            let users = 
                10
                |> pickMaleAndFemales rnd
                |> List.toArray
                |> Array.map (_createUser)
                
            let messages = users |> Array.map (EventhubMessage.Create "1.0.1")

            let tee f x =
                f x
                x
            let! u = 
                messages 
                |> Array.map( tee (printfn "%A") )
                |> Array.map(addToEH) 
                |> Task.WhenAll 
            return OkObjectResult(messages) :> IActionResult
        }
        
        //|> Async.StartAsTask