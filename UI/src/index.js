async function getData(params) {
    const data = await eel.main(
        params // Pass params to main function
    )()
    return data;
};