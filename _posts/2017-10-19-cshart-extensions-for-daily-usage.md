---
title:  "C# extensions for daily usage"
description: "List of C# extensions for daily usage. I am using them in my projects"
modified: 2017-10-19T22:40:00-03:00
tags:
  - dot.net
  - .net core
  - open source
---
Hi everyone! Today I want to share my extensions which I am using in my daily routine.

I want to say, that I used them in every standalone project I worked for (and sometimes job projects)
<a href="https://github.com/CodeBeavers/EverydayExtensionsCsharp">Go and grab them</a>

I **won't** update this article in the future. So, check link above for getting newest ones.

## Collection extensions

```csharp
public static List<T> NullToEmpty<T>(this List<T> source)
{
    return source ?? new List<T>();
}
```

```csharp
public static T[] ExpandArray<T>(this T[] array, T item)
{
    if (array == null || array.Length == 0)
    {
        array = new[] { item };
        return array;
    }

    var expandedArray = new T[array.Length + 1];
    Array.Copy(array, expandedArray, array.Length);
    expandedArray[array.Length] = item;

    return expandedArray;
}
```

## String's extensions

```csharp
public static bool IsNullOrEmpty(this string value)
{
    return string.IsNullOrEmpty(value);
}
```

```csharp
public static bool NotNullOrEmpty(this string value)
{
    return !string.IsNullOrEmpty(value);
}
```

## Json helpers (JSON.NET is required)

```csharp
public static string ToJson<T>(this T obj)
{
    return JsonConvert.SerializeObject(obj, Formatting.Indented);
}
```

## Entity Framework

```csharp
public static IQueryable<TEntity> Includes<TEntity>(this IQueryable<TEntity> source, 
    params Expression<Func<TEntity, object>>[] includes)
    where TEntity : class
{
    foreach (var include in includes)
    {
        source = source.Include(include);
    }
    
    return source;
}
```

## Conclusion

That's all. I'll be happy, If this link helps you. 