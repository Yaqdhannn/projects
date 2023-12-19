function Message(){
    const name = 'Dan yo Daan';
    if (name)
        return <h1>Hello {name}</h1>;
    return <h1>Alright then.. keep your secrets.</h1>;
}

export default Message;