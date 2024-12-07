class Tag:
    class Inline:
        def __new__(cls, *args, **kwargs):
            attrs = []
            for kwarg in kwargs.keys():
                if kwarg == "class_":
                    attrs.append(f'class="{kwargs[kwarg]}"')
                else:
                    attrs.append(f'{kwarg}="{kwargs[kwarg]}"')

            return f"<{cls.__name__.lower()}{' ' if len(attrs) > 0 else ''}{' '.join(attrs)}/{''.join(args) if args else ''}>"

    class BlockLevel:
        def __new__(cls, *args, **kwargs):
            attrs = ""
            content = ""
            for kwarg in kwargs.keys():
                if kwarg == "class_":
                    attrs = attrs + f'class="{kwargs[kwarg]}" '
                else:
                    attrs = attrs + f'{kwarg}="{kwargs[kwarg]}" '
                    
            for arg in args:
                content = content + arg

            return f"<{cls.__name__.lower()}{ ' ' if len(attrs) > 0 else '' }{attrs}>{ content }</{cls.__name__.lower()}>"