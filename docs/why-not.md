## Why not?

> 🤔 Why not put your business logic in APIs / Views / Serializers / Forms?

Relying on generic APIs / Views, with the combination of serializers & forms does 2 major things:

1. Fragments the business logic in multiple places, making it really hard to trace the data flow.
2. Hides things from you. In order to change something, you need to know the inner-workings of the abstraction that you are using.

Generic APIs & Views, in combination with serializers & forms, is really great for the straightforward "CRUD for a model" case.

From our experience, so far, this straightforward case rarely happens. **And once you leave the happy CRUD path, things start to get messy.**

And once things start to get messy, you need more "boxes", to organize your code in a better way.

This styleguide aims to:

1. Give you those "boxes".
1. Help you figure out your own "boxes", for your own specific context & needs.

Additionally, thanks to this comment - https://github.com/HackSoftware/Django-Styleguide/issues/170 - there's one additional way of looking at this:

The way your app should behave (or as we call it - "business logic") should not be related to the way you interface with it (be it an API, a management command or something else) and this is a very clear line, where we want to separate our concerns.

Of course, there are cases, where things can get intertwined, yet, a good baseline for thinking about this separation is - "core" vs. "interface".

---

> 🤔 Why not put your business logic in custom managers and/or querysets?

This is actually a good idea & you might introduce custom managers & querysets, that can expose better API, tailored to your domain.

But trying to place all of your business logic in a custom manager is not a great idea, because of the following:

1. Business logic has its own domain, which is not always directly mapped to your data model (models)
1. Business logic most often spans across multiple models, so it's really hard to choose where to place something.
   - Let's say you have a custom piece of logic that touches models `A`, `B`, `C`, and `D`. Where do you put it?
1. There can be additional calls to 3rd party systems. You don't want those in your custom manager methods.

**The idea is to let your domain live separately from your data model & API layer.**

If we take the idea of having custom queryset/managers and combine that with the idea of letting the domain live separately, we'll end up with what we call a "service layer".

**Services can be functions, classes, modules, or whatever makes sense for your particular case.**

With all that in mind, custom managers & querysets are very powerful tools and should be used to expose better interfaces for your models.

---

> 🤔 Why not put your business logic in signals?

From all of the available options, perhaps, this one will lead you to a very bad place very quickly:

1. Signals are a great tool for **connecting things that should not know about each other, yet, you want them to be connected.**
1. Signals are also a great tool **for handling cache invalidation** outside your business logic layer.
1. If we start using signals for things that are heavily connected, we are just making the connection more implicit and making it harder to trace the data flow.

That's why we recommend using signals for very particular use cases, but generally, **we don't recommend using them for structuring the domain / business layer.**