import React, { useState, useEffect } from 'react'
import axios from 'axios'
import 'bootstrap/dist/css/bootstrap.min.css'

interface Laptop {
	id: number
	title: string
	model: string
	price: number
	description: string
	owner: number
}

interface User {
	id: number
	username: string
	avatar: string
}

interface LoginForm {
	username: string
	password: string
}

interface RegisterForm {
	username: string
	password: string
	email: string
}

interface UpdateForm {
	newUsername: string
	newAvatar: File | null
}

interface LaptopsForm {
	title: string
	model: string
	price: number
	description: string
}

const App = () => {
	const [user, setUser] = useState<User | null>(null)
	const [laptops, setLaptops] = useState<Laptop[]>([])
	const [selectedLaptop, setSelectedLaptop] = useState<Laptop | null>(null)
	const [isViewingLaptop, setIsViewingLaptop] = useState(false)

	const [loginForm, setLoginForm] = useState<LoginForm>({
		username: '',
		password: '',
	})
	const [registerForm, setRegisterForm] = useState<RegisterForm>({
		username: '',
		password: '',
		email: '',
	})
	const [laptopsForm, setLaptopsForm] = useState<LaptopsForm>({
		title: '',
		model: '',
		price: 0,
		description: '',
	})

	const [username, setUsername] = useState(user?.username || '')
	const [avatar, setAvatar] = useState(user?.avatar || '')

	const [token, setToken] = useState(localStorage.getItem('token') || '')
	const [refreshToken, setRefreshToken] = useState(
		localStorage.getItem('refreshToken') || ''
	)

	const API_URL = 'http://127.0.0.1:8000/'

	const refreshAuthToken = async () => {
		if (!refreshToken) return

		try {
			const response = await axios.post(`${API_URL}auth/token/refresh/`, {
				refresh: refreshToken,
			})
			localStorage.setItem('token', response.data.access)
			setToken(response.data.access)
		} catch (error) {
			console.error('Ошибка обновления токена', error)
			logout()
		}
	}

	const login = async (e: React.FormEvent<HTMLFormElement>) => {
		e.preventDefault()
		try {
			const response = await axios.post(`${API_URL}auth/login/`, {
				username: loginForm.username,
				password: loginForm.password,
			})
			setToken(response.data.access)
			setRefreshToken(response.data.refresh)
			localStorage.setItem('token', response.data.access)
			localStorage.setItem('refreshToken', response.data.refresh)
			fetchUser()
		} catch (error) {
			console.error('Ошибка входа', error)
		}
	}

	const register = async (e: React.FormEvent<HTMLFormElement>) => {
		e.preventDefault()
		try {
			const response = await axios.post(`${API_URL}auth/register/`, {
				username: registerForm.username,
				password: registerForm.password,
				email: registerForm.email,
			})
			console.log('Пользователь зарегистрирован', response.data)
			alert('Регистрация прошла успешно! Теперь вы можете войти в систему.')
		} catch (error) {
			console.error('Ошибка регистрации', error)
		}
	}

	const logout = () => {
		setUser(null)
		setToken('')
		setRefreshToken('')
		localStorage.removeItem('token')
		localStorage.removeItem('refreshToken')
	}

	const fetchUser = async () => {
		if (!token) {
			console.log('Токен отсутствует')
			return
		}

		try {
			const response = await axios.get(`${API_URL}auth/user/`, {
				headers: { Authorization: `Bearer ${token}` },
			})
			setUser(response.data)
			fetchUserLaptops(response.data.id)
		} catch (error) {
			console.error('Ошибка получения пользователя', error)
			setToken('')
			localStorage.removeItem('token')
			setUser(null)
		}
	}

	const fetchLaptops = async () => {
		try {
			const response = await axios.get(`${API_URL}items/items/`)
			setLaptops(response.data)
		} catch (error) {
			console.error('Ошибка загрузки ноутбуков', error)
		}
	}

	const fetchUserLaptops = async (userId: number) => {
		try {
			const response = await axios.get(`${API_URL}items/items/?owner=${userId}`)
			setLaptops(response.data)
		} catch (error) {
			console.error('Ошибка загрузки ноутбуков пользователя', error)
		}
	}

	const createLaptop = async (e: React.FormEvent<HTMLFormElement>) => {
		e.preventDefault()
		if (!token) {
			console.log('Токен отсутствует')
			return
		}

		try {
			const response = await axios.post(
				`${API_URL}items/items/`,
				{
					title: laptopsForm.title,
					model: laptopsForm.model,
					price: laptopsForm.price,
					description: laptopsForm.description,
				},
				{
					headers: { Authorization: `Bearer ${token}` },
				}
			)
			setLaptops([...laptops, response.data])
		} catch (error) {
			console.error('Ошибка создания ноутбука', error)
		}
	}

	const deleteLaptop = async (id: number) => {
		if (!token) {
			console.log('Токен отсутствует')
			return
		}

		try {
			await axios.delete(`${API_URL}items/items/${id}/`, {
				headers: { Authorization: `Bearer ${token}` },
			})
			setLaptops(laptops.filter(laptop => laptop.id !== id))
		} catch (error) {
			console.error('Ошибка удаления ноутбука', error)
		}
	}

	const handleLoginChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		setLoginForm({ ...loginForm, [e.target.name]: e.target.value })
	}

	const handleRegisterChange = (
		e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
	) => {
		setRegisterForm({ ...registerForm, [e.target.name]: e.target.value })
	}

	const handleLaptopClick = (laptop: Laptop) => {
		setSelectedLaptop(laptop)
		setIsViewingLaptop(true)
	}

	const closeLaptopDetails = () => {
		setIsViewingLaptop(false)
		setSelectedLaptop(null)
	}

	const handleLaptopsFormChange = (
		e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
	) => {
		setLaptopsForm({ ...laptopsForm, [e.target.name]: e.target.value })
	}

	useEffect(() => {
		fetchLaptops()
		if (token) {
			fetchUser()
		}
	}, [token])

	const [updateForm, setUpdateForm] = useState<UpdateForm>({
		newUsername: '',
		newAvatar: null,
	})

	const handleUsernameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		setUpdateForm({ ...updateForm, newUsername: e.target.value })
	}

	const handleAvatarChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		setUpdateForm({ ...updateForm, newAvatar: e.target.files?.[0] || null })
	}

	const updateUserProfile = async (e: React.FormEvent<HTMLFormElement>) => {
		e.preventDefault()
		const formData = new FormData()
		if (updateForm.newUsername)
			formData.append('username', updateForm.newUsername)
		if (updateForm.newAvatar) formData.append('avatar', updateForm.newAvatar)

		try {
			const response = await axios.patch(`${API_URL}auth/user/`, formData, {
				headers: {
					Authorization: `Bearer ${token}`,
					'Content-Type': 'multipart/form-data',
				},
			})
			setUser(response.data)
			setUsername(response.data.username)
			setAvatar(response.data.avatar)
			alert('Profile updated!')
		} catch (error) {
			console.error('Error updating profile', error)
		}
	}

	return (
		<div className='container mt-4'>
			<h1>Магазин ноутбуков</h1>

			{!isViewingLaptop && (
				<>
					<h3 className='mt-4'>Ноутбуки</h3>
					<ul className='list-group'>
						{laptops.map(laptop => (
							<li
								key={laptop.id}
								className='list-group-item d-flex justify-content-between align-items-center'
								onClick={() => handleLaptopClick(laptop)}
								style={{ cursor: 'pointer' }}
							>
								<div>
									<strong>{laptop.title}</strong> - {laptop.model} -{' '}
									{laptop.price}₴
								</div>
								{user && user.id === laptop.owner && (
									<button
										onClick={() => deleteLaptop(laptop.id)}
										className='btn btn-danger btn-sm'
									>
										Удалить
									</button>
								)}
							</li>
						))}
					</ul>
				</>
			)}

			{isViewingLaptop && selectedLaptop && (
				<div className='mt-4'>
					<h4>{selectedLaptop.title}</h4>
					<p>
						<strong>Модель:</strong> {selectedLaptop.model}
					</p>
					<p>
						<strong>Цена:</strong> {selectedLaptop.price}₴
					</p>
					<p>
						<strong>Описание:</strong> {selectedLaptop.description}
					</p>
					<p>
						<strong>Владелец:</strong> {selectedLaptop.owner}
					</p>
					<button
						onClick={closeLaptopDetails}
						className='btn btn-secondary mt-2'
					>
						Закрыть
					</button>
				</div>
			)}

			{!user ? (
				<div>
					<form onSubmit={login} className='mt-4'>
						<h2>Вход</h2>
						<input
							type='text'
							name='username'
							placeholder='Имя пользователя'
							value={loginForm.username}
							onChange={handleLoginChange}
							className='form-control mb-2'
						/>
						<input
							type='password'
							name='password'
							placeholder='Пароль'
							value={loginForm.password}
							onChange={handleLoginChange}
							className='form-control mb-2'
						/>
						<button type='submit' className='btn btn-primary'>
							Войти
						</button>
					</form>

					<form onSubmit={register} className='mt-4'>
						<h2>Регистрация</h2>
						<input
							type='text'
							name='username'
							placeholder='Имя пользователя'
							value={registerForm.username}
							onChange={handleRegisterChange}
							className='form-control mb-2'
						/>
						<input
							type='password'
							name='password'
							placeholder='Пароль'
							value={registerForm.password}
							onChange={handleRegisterChange}
							className='form-control mb-2'
						/>
						<input
							type='email'
							name='email'
							placeholder='Email'
							value={registerForm.email}
							onChange={handleRegisterChange}
							className='form-control mb-2'
						/>
						<button type='submit' className='btn btn-success'>
							Зарегистрироваться
						</button>
					</form>
				</div>
			) : (
				<div>
					<h2>Привет, {user.username}</h2>
					<button onClick={logout} className='btn btn-danger mb-4'>
						Выйти
					</button>

					<h3>Мои объявления</h3>
					<ul className='list-group'>
						{laptops
							.filter(laptop => laptop.owner === user.id)
							.map(laptop => (
								<li
									key={laptop.id}
									className='list-group-item d-flex justify-content-between align-items-center'
								>
									<div>
										<strong>{laptop.title}</strong> - {laptop.model} -{' '}
										{laptop.price}₴
									</div>
									<button
										onClick={() => deleteLaptop(laptop.id)}
										className='btn btn-danger btn-sm'
									>
										Удалить
									</button>
								</li>
							))}
					</ul>

					<form onSubmit={createLaptop}>
						<h3>Добавить ноутбук</h3>
						<input
							type='text'
							name='title'
							placeholder='Название'
							value={laptops.title}
							onChange={handleRegisterChange}
							className='form-control mb-2'
						/>
						<input
							type='text'
							name='model'
							placeholder='Модель'
							value={laptops.model}
							onChange={handleRegisterChange}
							className='form-control mb-2'
						/>
						<input
							type='number'
							name='price'
							placeholder='Цена'
							value={laptops.price}
							onChange={handleRegisterChange}
							className='form-control mb-2'
						/>
						<textarea
							name='description'
							placeholder='Описание'
							value={laptops.description}
							onChange={handleRegisterChange}
							className='form-control mb-2'
						/>
						<button type='submit' className='btn btn-primary'>
							Добавить
						</button>
					</form>

					<h3 className='mt-4'>
						Изменить профиль(Времено не работает идите нахуй хуй вам а не менять
						профиль если надо изменить очень надо пишите @sharkikos)
					</h3>
					<form onSubmit={updateUserProfile}>
						<input
							type='text'
							name='newUsername'
							placeholder='Новое имя пользователя'
							value={updateForm.newUsername}
							onChange={handleUsernameChange}
							className='form-control mb-2'
						/>
						<input
							type='file'
							name='avatar'
							onChange={handleAvatarChange}
							className='form-control mb-2'
						/>
						<button type='submit' className='btn btn-warning'>
							Обновить профиль
						</button>
					</form>
				</div>
			)}
		</div>
	)
}

export default App
