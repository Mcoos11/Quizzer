import './TextInput.css'

function TextInput(props : any) {

    const type = props.type ? props.type : "text";

    return (
        <>
            <label className="input-label">
                <div>{props.children}</div>
                <input className="text-input" type={type} name={props.name} value={props.value} onChange={props.onChange}></input>
            </label>
        </>
     );
}

export default TextInput;