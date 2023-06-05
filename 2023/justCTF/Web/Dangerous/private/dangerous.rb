require "sinatra"
require "sqlite3"
require "erubi"
require "digest"
require "json"

config = JSON.parse(File.read("./config.json"))

set :bind, '0.0.0.0'
enable :sessions
set :erb, :escape_html => true

con = SQLite3::Database.new "sqlite.db"

con.execute "CREATE TABLE IF NOT EXISTS threads(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT,
        ip TEXT,
        username TEXT
    );"

con.execute "CREATE TABLE IF NOT EXISTS replies(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT,
        ip TEXT,
        username TEXT,
        thread_id INTEGER
    );"

def get_threads(con)
  return con.execute("SELECT * FROM threads ORDER BY id DESC;")
end

def get_replies(con, id)
  return con.execute("SELECT *, null, 0 as p FROM threads WHERE id=? 
                    UNION SELECT *, 1 as p FROM replies WHERE thread_id=? order by p", [id, id])
end

def is_allowed_ip(username, ip, config)
  return config["mods"].any? {
    |mod| mod["username"] == username and mod["allowed_ip"] == ip
  }
end


get "/" do
  @threads = get_threads(con)
  erb :index
end

post "/thread" do
  if params[:content].nil? or params[:content] == "" then
    raise "Thread content cannot be empty!"
  end
  if session[:username] then
    username = is_allowed_ip(session[:username], request.ip, config) ? session[:username] : nil
  end
  # === temporarily disabled ===
  # con.execute("INSERT INTO threads (id, content, ip, username)
  #           VALUES (?, ?, ?, ?)", [nil, params[:content], request.ip, username])
  redirect to("/#{con.execute('SELECT last_insert_rowid()')[0][0]}")
end

get "/flag" do
  if !session[:username] then
    erb :login
  elsif !is_allowed_ip(session[:username], request.ip, config) then
    return [403, "You are connecting from untrusted IP!"]
  else
    return config["flag"] 
  end
end

post "/login" do
  if config["mods"].any? {
    |mod| mod["username"] == params[:username] and mod["password"] == params[:password]
  } then
    session[:username] = params[:username]
    redirect to("/flag")
  else
    return [403, "Incorrect credentials"]
  end
end

get "/:id" do
  @id = params[:id]
  @replies = get_replies(con, @id)
  erb :thread
end

post "/:id" do
  if params[:content].nil? or params[:content] == "" then
    raise "Reply content cannot be empty!"
  end
  if session[:username] then
    username = is_allowed_ip(session[:username], request.ip, config) ? session[:username] : nil
  end
  @id = params[:id]
  # === temporarily disabled ===
  # con.execute("INSERT INTO replies (id, content, ip, username, thread_id)
  #             VALUES (?, ?, ?, ?, ?)", [nil, params[:content], request.ip, username, @id])
  redirect to("/#{@id}")
end
