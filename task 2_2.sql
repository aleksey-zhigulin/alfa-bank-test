select 
	credit as 'Сумма кредита',
    age as 'Возраст',
    income as 'Доход',
	status as 'Статус',
    decision as 'Решение',
    rejection_reason as 'Причина отказа'
from credit_request
    join form on credit_request.idrequest = form.idform
where partner=3