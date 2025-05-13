const doSomething = (cb) => {
    const error = new Error('Something went wrong lol');
    const result = 'It worked!';
    cb(null, result);
};

doSomething((error, result) => {
    if (error) {
        console.log('There was an error lol');
        return;
    }
    console.log('Everything went well');
});