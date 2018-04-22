---
title:  "The problems with combining attribute routes in ASP.NET Core"
description: "How to solve and tine reminder to myself "
modified: 2018-04-19T15:24:00-03:00
tags:
  - .net
  - asp.net core
---

Hello everyone!

Currently I am developing an api with using of ASP.NET Core. Two days ago I notices that my route didn't combine (I am using route attributes).

So, I was writing something like in the code block below.


```csharp
    [Route("users")]
    public class UserController : Controller
    {
        [Route("/{userId}/email")]
        public async Task UpdateEmail(int userId, [FromBody]UpdateEmailRequest request)
        {
            ...
        }
    }
```

And for the controller and the routes I've got `/{userId}/email` not `users/{userId}/email`.
The problem was in the `/` before the child route.

So, the solution is 

```csharp
    [Route("users")]
    public class UserController : Controller
    {
        [Route("{userId}/email")]
        public async Task UpdateEmail(int userId, [FromBody]UpdateEmailRequest request)
        {
            ...
        }
    }
```

## Conclusion

That’s all, thank you for you attention!
