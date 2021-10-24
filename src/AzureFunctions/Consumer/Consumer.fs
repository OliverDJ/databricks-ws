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
0
//[<FunctionName("EventhubReader")>]
//let consume ([<EventHubTrigger(eventHubName = "",
//                                Connection = "eventhubreader",
//                                ConsumerGroup = "$Default")>] msg: EventData,
//              log: ILogger) =
//    task {

//        printfn "hello!"
//        return 0
//    }