declare module 'auth' {
    export function login(email: string, password: string): Promise<void>;
}