import neo4j from 'neo4j-driver'

const uri = "neo4j+s://4082bfae.databases.neo4j.io";
const user = "neo4j";
const password = "HS1hNLNNGI6P3gHiWc2F9YH9EoZZoOAPgNzkPbhbBm8";

const driver = neo4j.driver(uri, neo4j.auth.basic(user, password));

export const getSession = () => {
    return driver.session();
}
