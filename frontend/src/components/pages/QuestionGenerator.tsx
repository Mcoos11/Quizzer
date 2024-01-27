import './QuestionGenerator.css'
import Button from '../Button.tsx'
import TextInput from '../TextInput.tsx';
import { FormEvent } from 'react';
import Select from 'react-select'

import React, { useState } from 'react';
import { connect } from 'react-redux';
import { generate } from '../../actions/generator.tsx';
import store from '../../store'


function QuestionGenerator() {
    
    // const [formData, setFormData] = useState({
    //     questions_number: '',
    //     topic: '',
    //     answers_number: '',
    //     url: '',
    // });

    // const { questions_number, topic, answers_number, url } = formData;
    // const onChange = (e: any) => setFormData({ ...formData, [e.target.name]: e.target.value });
    // const onSubmit = (e: any) => {
    //     e.preventDefault();
    //     generate(questions_number, topic, answers_number, url);
    // }

    const q_options = [
        { value: '1', label: '1' },
        { value: '2', label: '2' },
        { value: '3', label: '3' },
        { value: '4', label: '4' },
        { value: '5', label: '5' },
        { value: '6', label: '6' },
        { value: '7', label: '7' }
      ]
    const ans_options = [
        { value: '1', label: '1' },
        { value: '2', label: '2' },
        { value: '3', label: '3' },
        { value: '4', label: '4' },
        { value: '5', label: '5' },
        { value: '6', label: '6' }
    ]

    return (
        <>
            <form className="login-form" action='question_generator/generate_XML/' method='POST'>
                <h1>Generowanie pytań</h1>
                <TextInput
                        name='topic'>Temat</TextInput>
                <label htmlFor="q_no_imput">
                Liczba pytań
                </label>
                <Select options={q_options} name='questions_number' inputId="q_no_imput"  /><br></br>
                <label htmlFor="ans_no_imput">
                Liczba odpowiedzi w jednym pytaniu
                </label>
                <Select name='answers_number' inputId="ans_no_imput" options={ans_options} /><br></br>
                <TextInput 
                        name='url'>Strona internetowa (opcjonalnie)</TextInput>
                <Button className="primary" type="submit">Generuj</Button>
            </form>
        </>
    )
}

export default QuestionGenerator;