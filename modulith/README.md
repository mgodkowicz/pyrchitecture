# Modulith
#### Modular Monolith

## Rules
- Modules have to be independents
- No imports from inside of modules - only exposed APIs
- Communication only with facades/apis or async with event publisher.
- No Foreign Keys between modules data.
- Injector for dependency injection.
- Keep a common module as small as possible.
- Consider creating many Django apps in one module.
- Think about modules as microservices but deployable as single unit.

