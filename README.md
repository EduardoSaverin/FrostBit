# FrostBit
----
FrostBit is a distributed unique ID generator inspired by [Twitter's Snowflake](https://blog.twitter.com/2010/announcing-snowflake).

FrostBit focuses on lifetime and performance on many host/core environment. So it has a different bit assignment from Snowflake. A FrostBit ID is composed of

```text
39 bits for time in units of 10 msec
8 bits for a sequence number
16 bits for a machine id
```

As a result, FrostBit has the following advantages and disadvantages:

- The lifetime (174 years) is longer than that of Snowflake (69 years)
- It can work in more distributed machines (2^16) than Snowflake (2^10)
- It can generate 2^8 IDs per 10 msec at most in a single machine/thread (slower than Snowflake)
However, if you want more generation rate in a single host, you can easily run multiple FrostBit ID generators concurrently.

## License
----
The MIT License (MIT)
See [LICENSE](https://github.com/sony/sonyflake/blob/master/LICENSE) for details.