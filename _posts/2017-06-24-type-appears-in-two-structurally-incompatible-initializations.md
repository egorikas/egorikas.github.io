---
title:  "Solving of 'The type appears in two structurally incompatible initializations within a single LINQ to Entities query' problem"
description: "Solving of 'The type appears in two structurally incompatible initializations within a single LINQ to Entities query' problem"
modified: 2017-06-24T12:14:00-03:00
tags:
  - entify framework
  - linq
---
Hi everyone! Today I want to talk about solving the 'The type appears in two structurally incompatible initializations within a single LINQ to Entities query' problem.

A few weeks ago, I faced off a horrified problem, my `LINQ to Entities query` didn't work and threw an exception:

System.NotSupportedException: 'The type '***' appears in two structurally incompatible initializations within a single LINQ to Entities query. 
A type can be initialized in two places in the same query, but only if the same properties are set in both places and those properties are set in the same order.'
{: .notice--warning}

It was tought for me to find the answer, so I decided share it with you.

### How did I get it?

Let's imagine that we have two tables in a database, which contain different domain entities. 
There is a possibility that we will have to getting some info from them for joininig (for my case, I was creating a report system).
I'm not allowed to write article about that real case, but I am trying to do this with examples. So, there are two classes `A` and `B`.

```csharp 			
    public class A
    {
        public string Name { get; set;}
        public string Rating { get; set;}
    }
```

```csharp 			
    public class B
    {
        public string Name { get; set;}
        public bool? IsSelected { get; set;}
    }
```

And we want to get an instance of class C, which is union of A and B.

```csharp 			
    public class C
    {
        public string Name { get; set;}
        public string Rating { get; set;}
        public bool? IsSelected { get; set;}		
    }
```

So, I decided not to use a raw `SQL-request`. Instead of it, I used a `LINQ to Entities query`.

```csharp 
    public List<C> UnionThem(){
		var firstPart = _context.A.Select(x => {
			Name = x.Name,
			IsSelected = null,
			Rating = x.Rating
		});
		
		var secondPart = _context.B.Select(x => {
			Rating = null,
			IsSelected = x.IsSelected,
			Name = x.Name
		});	
		
		return firstPart.Union(secondPart).ToList();	
	}			
```

If you try to run this code, it will thrown 'The type appears in two structurally incompatible initializations within a single LINQ to Entities query' exception.

### Solvation

So, in my case solvation was simple. Variables in `Select` statement were in a wrong order. When I put them in the same order for both `Select`, this query started to work.

```csharp 
    public List<C> UnionThem(){
		var firstPart = _context.A.Select(x => {
			Name = x.Name,
			Rating = x.Rating,
			IsSelected = null
		});
		
		var secondPart = _context.B.Select(x => {
			Name = x.Name,
			Rating = x.Rating,
			IsSelected = null
		});	
		
		return firstPart.Union(secondPart).ToList();	
	}			
```

### Thoughts

I didn't find 100% correct answer why this happens. So, text below is just a result of my thoughts and seeing code of `Entity Framework`.

When `EF` builds a request to database, it parses the linq query to the raw SQL query. So, in the right case, the linq query above translates to 

```sql
SELECT
  Name,
  Rating,
  IsSelected
FROM (
  (
    SELECT
      Name,
      Rating,
      IsSelected
    FROM TableA
  )
  UNION ALL
  (
    SELECT
      Name,
      Rating,
      IsSelected
    FROM TableB
  )
)
```
When you have disordered statements EF gets crazy and can't translate them to the SQL. So, I think that the reason of problems is disordered arguments.

**Please Note:**  You can EF source code on <a href="https://github.com/aspnet/EntityFramework6">github</a>.
{: .notice--info}

### Conclusion

That's all. I'll be happy, If this article helps you. 