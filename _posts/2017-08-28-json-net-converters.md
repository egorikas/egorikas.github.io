---
title:  "Unix timestamp and boolean converters for Json.NET"
description: "The most useful additional converters for Json.net"
modified: 2017-08-28T10:30:00-03:00
tags:
  - dot.net
  - json.net
  - opensource
  - tools
---
Hi everyone! Today I want to talk about two little additional converters for `Json.NET` which can make your life easier and more fun.

A few weeks ago, I decided to wrote a simple api-consumer. While I was creating this app I found some problems with transformation data from json to objects.
For solving them I created two converters for `Json.NET`

### Unix timestamp to DateTime

An api returns dates in format of unix timestamps, So, what should we do? Exactly, create our own `custom converter`. I did all the job for you. You can grab it from `nuget`

`Install-Package UnixTimeConverter`

or get it from <a href="https://github.com/egorikas/UnixTimeConverter">Github</a> and change code if you want. But it will be better, if you create a `pr` ;)

#### Example of UnixTimeConverter usage

```csharp
namespace UsageExample
{
    public class ApiData
    {
        [JsonConverter(typeof(UnixTimeConverter))]
        public DateTime Date { get; set; }
    }

    public class ConverterTest
    {
        [Fact]
        public void HappyPath()
        {
            //Arrange
            var apiJson = "{ Date : 1321009871 }";

            //Act
            var result = JsonConvert.DeserializeObject<ApiData>(apiJson);

            //Assert
            Assert.Equal(new DateTime(2011, 11, 11, 11, 11, 11, DateTimeKind.Utc), result.Date);
        }
    }
}
```

### Number to bool converter for Json.NET
My second problem was about converting `booleans` from `numbers`. It's a common situation when endpoint returns `"bool"` values as 1 or 0.
So, I've solved this problem too. You can install `converter`

`Install-Package BooleanConverter`

or get it from <a href="https://github.com/egorikas/BooleanConverter">Github</a>

#### Example of BooleanConverter usage

```csharp
namespace UsageExample
{
    public class ApiData
    {
        [JsonConverter(typeof(BooleanConverter))]
        public bool Field { get; set; }
    }

    public class ConverterTest
    {
        [Fact]
        public void SerializeHappyPath()
        {
            //Arrange
            var apiJson = "{ Field : 1}";

            //Act
            var result = JsonConvert.DeserializeObject<ApiData>(apiJson);

            //Assert
            Assert.Equal(true, result.Field);
        }
    }
}
```
### P.S.
I asked maintainer `Json.NET` about `PR` with converters to the library. But I was given an answer, that he didn't like the idea of adding code to core library due to size issues.

<a href="https://github.com/JamesNK/Newtonsoft.Json/issues/1387">Github's issue</a>


### Conclusion

That's all. I'll be happy, If this article and tools helps you. 