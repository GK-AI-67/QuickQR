declare module 'axios' {
  export interface AxiosResponse<T = any> { data: T }
  const axios: any
  export default axios
}


