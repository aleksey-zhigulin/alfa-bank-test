select 
	idpartner as 'ID партнера', 
	count(credit_request.idrequest) as 'Количество заявок',
    count(
		case 
			when credit_request.decision = 'Y' then 1
            else null
		end
	) as 'Количество одобренных заявок',
    count(
		case 
			when credit_request.decision = 'N' then 1
            else null
		end
	) as 'Количество отказов',
    sum(
		case 
			when credit_request.decision = 'Y' then form.credit
            else 0
		end
	) as 'Сумма выданных кредитов'
from partner 
    left join credit_request on idpartner = partner
	left join form on credit_request.idrequest = form.idform
group by idpartner;