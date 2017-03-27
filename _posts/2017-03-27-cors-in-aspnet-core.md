---
title:  "CORS in ASP.NET CORE"
modified: 2017-03-27T00:10:00-03:00
categories: 
  - Web
tags:
  - ASP.NET
  - NET.CORE
  - AngularJs
---

In my spare time I am writing applications with technologies, which are newer than my job project's ones.
So, I decided to build a simple app using `ASP.NET CORE` and `AngularJs` (version 2).

In the time of writting this project, I was getting a strange behaivor of my requests from `javascript` to `server-side`.

```javascript
    let body: any = {"Email": "value1", "Password": "value2"};
    let url = "http://localhost:5000/api/user/login";
    let response: any;
    let headers = new Headers({'Content-Type': 'application/json'});
    let options = new RequestOptions({headers: headers});
    this.http.post(url, body, options).subscribe(
      data => {
        response = data
      },
      err => console.error(err),
      () => {
        console.log(response)
      });
```



My code didn't want to set custom `Content-type` headers. When I send a request, I got `415 (Unsupported Media Type)` and `No 'Access-Control-Allow-Origin' header is present` 
exception in console.


### Errors' screenshot

<figure>
	<a href="/assets/images/2017-03-26_22-45-27.png"><img src="/assets/images/2017-03-26_22-45-27.png"></a>
	<figcaption>Screenshot of Google Chrome's console</figcaption>
</figure>


### Searching for solution

First of all, I thought about problems with `HttpModule` of `Angular`. I even created a <a href="http://stackoverflow.com/questions/42749192/angular2-http-cant-send-post-with-body-and-set-content-type/">stackoverflow question</a>.
Then, I started to think that the problem may be at the server side. And it was. I had forgotten to set up `CORS` settings for for my back-end app.

### Configuring CORS for ASP.NET CORE

First of all installing of `Microsoft.AspNetCore.Cors` is required. You can do this by GUI or just run `Install-Package Microsoft.AspNetCore.Cors` in Package Manager Console.
Then you should  modify your `Startup.cs`.

### Step 1. Modify `ConfigureServices` method

You need add some code to your `ConfigureServices` method

```csharp
 public void ConfigureServices(IServiceCollection services)
 {
    //CORS
    var corsBuilder = new CorsPolicyBuilder();
    corsBuilder.AllowAnyHeader();
    corsBuilder.AllowAnyMethod();
    corsBuilder.AllowAnyOrigin(); // For everyone
	
    // If you want to set up a special origin
    //corsBuilder.WithOrigins("http://localhost:1111"); 

    corsBuilder.AllowCredentials();

    services.AddCors(options =>
    {
        options.AddPolicy("MyCorsPolicy", corsBuilder.Build());
    });

	// other stuff
  }
```

### Step 2. Modify `Configure` method

Then you need to modify `Configure` method

```csharp
public void Configure(IApplicationBuilder app, 
					  IHostingEnvironment env, 
					  ILoggerFactory loggerFactory)
{
    app.UseCors("MyCorsPolicy");	
	// other stuff	
    app.UseMvc();
}
```

**Please Note:**  It's important to put `app.UseCors("MyCorsPolicy")` before `app.UseMvc()`. For details see <a href="https://docs.microsoft.com/en-us/aspnet/core/fundamentals/middleware">official docs</a>. 
{: .notice--danger}


### Conclusion

That's all. I'll be happy, If this article helps you. 

<a href="https://docs.microsoft.com/en-us/aspnet/core/security/cors">Docs about CORS in ASP.NET CORE</a>

