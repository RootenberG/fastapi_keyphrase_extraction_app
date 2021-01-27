if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.app.main:app", host="127.0.0.1",
                port=3053, reload=True, debug=True)
