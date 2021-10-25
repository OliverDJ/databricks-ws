module Consumer


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
open System.Text

let deserialize<'T> s = JsonConvert.DeserializeObject<'T>(s)


[<FunctionName("EventhubReader")>]
let consume ([<EventHubTrigger(eventHubName = "databricks-workshop",
                                Connection = "eventhubreader",
                                ConsumerGroup = "%consumergroup%")>] msg: EventData,
              log: ILogger) =
    task {
        let user = 
            msg 
            |> (fun m ->  Encoding.UTF8.GetString(m.Body.Array, m.Body.Offset, m.Body.Count))
            |> deserialize<EventhubMessage<Models.User>>


        user |> printfn "-> %A"
        return ()
    }