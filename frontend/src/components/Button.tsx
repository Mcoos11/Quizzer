import './Button.css'

function Button(props : any) {

    const buttonClass = 'btn ' + (props.className === undefined ? '' : props.className);

    if(props.link) {
        return (
            <a className={buttonClass} href={props.link}>{props.children}</a>
        );
    }else{
        return (
            <button className={buttonClass} onClick={props.onClick} type={props.type}>{props.children}</button>
        );
    }
}

export default Button;