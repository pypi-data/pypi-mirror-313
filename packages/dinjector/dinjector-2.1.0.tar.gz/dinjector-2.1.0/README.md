# Dependency Injector


## Description

Very simple dependency injector for constructing application from a yaml file.

## Installation

This project has an automated deployment to pypi, so only is needed to use pip command:

```
>> pip install dinjector
```

The injector needs a ConfigService class to get all application parameters. There is an implementation of it in project `config-srv`. The dependency is optional and you can inject anyone which comply the ConfigService interface.

## Usage

Once you have installed it, you'll have access to a package called `di` wher you only have to import `DependencyInjector` class.

The use of this library is by inheritance. If you want to create a Value Object you only have to inherit from a Value class. If you want to have an aggregate, inherit from a Aggregate class, if a service from a Service class.
## Support

Send any suggestion to sruiz@indoorclima.com or salvador.ruiz.r@gmail.com. Any ideas or support is well recieved.

## Roadmap

- [ ] Increment versioning when pushing
- [ ] Integrate with gitlab continuous integration to publish to pypi as library
- [ ] Improve coverage rate to > 96%
- [ ] Improve usage documentation with sphinx
- [ ] Upload to readthedocs

## Contributing
State if you are open to contributions and what your requirements are for accepting them.


## License

This is under LGPL lincense. You can use and modify this library. See details in [[LICENCE.txt]]

## Project status

It is used in projects developed currently by the company IndoorClima.
