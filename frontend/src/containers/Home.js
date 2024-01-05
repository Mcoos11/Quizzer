import React, {useEffect, useState} from 'react';
import { Link } from 'react-router-dom'

const Home = () => {
    const [response, setResponse] = useState(null);
  const [token, setToken] = useState(null);

  useEffect(() => {
    // Assuming you have a function to get the JWT token, e.g., from local storage
    const fetchedToken = localStorage.getItem('access');
    setToken(fetchedToken);
  }, []);

  const handleButtonClick = async () => {
    try {
      const headers = {
        'Content-Type': 'application/json',
        Authorization: `${token}`,
      };

      const response = await fetch('http://localhost:8002/api/courses', {
        method: 'GET',
        headers: headers,
      });

      if (response.ok) {
        const data = await response.json();
        setResponse(data);
      } else {
        console.error('Error fetching data:', response.statusText);
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };
    return (
        <div className='container'>
            <div className='p-5 mb-4 bg-light rounded-3'>
                <h1 className='display-4'>Witamy!</h1>
                <p className='lead'>Tutaj może być jakiś opis...</p>
                <hr className='my-4'/>
                <p>Tutaj też. LoginBtn -</p>
                <Link className='btn btn-primary btn-log' to='/login' role='button'>Logowanie</Link>
            </div>
            <div>
                <button onClick={handleButtonClick}>Fetch Data</button>
                {response && (
                    <div>
                        <h2>Response:</h2>
                        <pre>{JSON.stringify(response, null, 2)}</pre>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Home;