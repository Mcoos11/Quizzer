import './Registration.css'
import Button from '../Button.tsx'
import TextInput from '../TextInput.tsx';

function Registration() {

    return (
        <>
            <section className="login-form">
                <h1>Zarejestruj się</h1>
                <TextInput>Imię</TextInput>
                <TextInput>E-mail</TextInput>
                <TextInput type="password">Hasło</TextInput>
                <Button className="primary">Zarejestruj się</Button>
            </section>
        </>
    )
}

export default Registration;