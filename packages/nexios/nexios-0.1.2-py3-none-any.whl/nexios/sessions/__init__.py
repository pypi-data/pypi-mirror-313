try:
    import tortoise
    import aerich

except ImportError:
    raise ImportError("Tortoise orm and aerich is required to use session")



