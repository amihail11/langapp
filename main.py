if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.langapp.api.app:app", reload=True)
