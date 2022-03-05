from Controller.basic import check
from Object.liveconsent import liveconsent

def user_login(cn, nextc):
    err = check.contain(cn.pr, ["login", "password"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    cn.private["user"] = user()
    err = cn.private["user"].login(
        cn.pr["login"],
        cn.pr["password"]
    )
    return cn.call_next(nextc, err)
