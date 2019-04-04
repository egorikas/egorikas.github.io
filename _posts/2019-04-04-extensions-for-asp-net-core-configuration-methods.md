---
title:  "You should use extension methods for ASP.NET Core configuration methods"
description: "Thoughts about a configuration process of ASP.NET Core"
modified: 2019-04-04T16:26:00-03:00
tags:
  - asp.net core
  - .net core
---

Hi everyone! Today I want to talk about a configuration process of `ASP.NET Core`.

## Large projects and ASP.NET Core

In my experience looking through `ConfigureServices` in a big project is a really exhausting experience.
If your project uses `Swagger`, `EF` and `CORS`-configuration, I suppose, you alredy understand me.

## Using extensions for `ConfigureServices` methods

In my projects I tend to use extensions methods for `IServiceCollection` due to improvement of readability of `ConfigureServices` method.

Let's imagine, that we have a standard pack of configuration for ASP.NET Core application.

```csharp
        public void ConfigureServices(IServiceCollection services)
        {
            var corsBuilder = new CorsPolicyBuilder();
            corsBuilder.AllowAnyHeader();
            corsBuilder.AllowAnyMethod();
            corsBuilder.AllowAnyOrigin();
            corsBuilder.AllowCredentials();

            services.AddCors(options => { options.AddPolicy("MyCorsPolicy", corsBuilder.Build()); });

            services.AddDbContext<DotNetRuServerContext>(options =>
                options.UseSqlServer(configuration.GetConnectionString("Database")));

            services.AddTransient<IAuthService, AuthService>();

            services
                .AddMvc(options => { options.Filters.Add(typeof(ExceptionFilter)); })
                .AddJsonOptions(options =>
                {
                    options.SerializerSettings.Converters.Add(new Newtonsoft.Json.Converters.StringEnumConverter());
                    options.SerializerSettings.NullValueHandling = Newtonsoft.Json.NullValueHandling.Ignore;
                })
                .SetCompatibilityVersion(CompatibilityVersion.Version_2_2);


            services.AddSwaggerGen(c =>
            {
                c.CustomSchemaIds(x => x.FullName);
                c.SwaggerDoc("v1", new Info {Title = "Example", Version = "v1"});
                c.DescribeAllEnumsAsStrings();
            });
        }

```

Looks complicated? Yes, it does. But what if we put all the code to the extension methods of `IServiceCollection`?

```csharp

        public void ConfigureServices(IServiceCollection services)
        {
            services.ConfigureCors();
            services.ConfigureDependencies(_configuration);
            services.ConfigureMVC(_configuration);            
            services.ConfigureSwagger();
        }

        // Usually I put those methods to different files as Application/Extensions/DependencyExtensions.cs and etc
        public static void ConfigureMVC(this IServiceCollection services, IConfiguration configuration)
        {
            services
                .AddMvc(options => { options.Filters.Add(typeof(ExceptionFilter)); })
                .AddJsonOptions(options =>
                {
                    options.SerializerSettings.Converters.Add(new Newtonsoft.Json.Converters.StringEnumConverter());
                    options.SerializerSettings.NullValueHandling = Newtonsoft.Json.NullValueHandling.Ignore;
                })
                .SetCompatibilityVersion(CompatibilityVersion.Version_2_2);

        }

        public static void ConfigureSwagger(this IServiceCollection services)
        {
            services.AddSwaggerGen(c =>
            {
                c.CustomSchemaIds(x => x.FullName);
                c.SwaggerDoc("v1", new Info {Title = "DotNetRu", Version = "v1"});
                c.DescribeAllEnumsAsStrings();

                var security = new Dictionary<string, IEnumerable<string>>
                {
                    {"Bearer", new string[] { }},
                };
                c.AddSecurityDefinition("Bearer", new ApiKeyScheme
                {
                    Description =
                        "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\"",
                    Name = "Authorization",
                    In = "header",
                    Type = "apiKey"
                });
                c.AddSecurityRequirement(security);
            });
        }


        public static void ConfigureDependencies(this IServiceCollection services, IConfiguration configuration)
        {
            services.AddDbContext<DotNetRuServerContext>(options =>
                options.UseSqlServer(configuration.GetConnectionString("Database")));

            services.AddTransient<IAuthService, AuthService>();
        }

        public static void ConfigureCors(this IServiceCollection services)
        {
            var corsBuilder = new CorsPolicyBuilder();
            corsBuilder.AllowAnyHeader();
            corsBuilder.AllowAnyMethod();
            corsBuilder.AllowAnyOrigin();
            corsBuilder.AllowCredentials();

            services.AddCors(options => { options.AddPolicy("MyCorsPolicy", corsBuilder.Build()); });
        }
```
If you put those metods to the different files in your project structure, to my mind, reading code would be much easier
for a programmer. Because he see scoped code (like db configuration) and isn't bothered by swagger's stuff, for example.

## Conclusion

That’s all, thank you for you attention!
