import logging
import re
import requests
from telegram.ext import Updater, MessageHandler, Filters

API_KEY = 'YOUR API KEY'
# Set up the logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info('Starting Bot...')


def process_message(message, response_array, response):
    # Splits the message and the punctuation into an array
    list_message = re.findall(r"\w+|[^\w\s]", message)

    # Scores the amount of words in the message
    score = 0
    for word in list_message:
        if word in response_array:
            score += 1

    # Returns the response and the score of the response
    return score, response


def get_car_info(plate):
    try:
        response = requests.get(f'https://www.yakarouler.com/car_search/immat?immat={plate}&name=undefined&redirect=true')
        data = response.text
        finder_start = data.find('<h2 class="title-car">')
        car = data[finder_start+22:data.find('</h2>')]
        model = car[:car.find('(')]
        tab = car.split()
        for spec in tab:
            if '(' in spec and 'kw' not in spec:
                gen = spec
            elif '.' in spec:
                size = spec
            elif 'cv' in spec or 'CV' in spec:
                hp = spec
        return f"C'est un(e) {model} de {hp}"
    except:
        return ''


def get_response(message):
    # Add your custom responses here
    radar_priver = ['el-032-xa','ez-254-bp', 'ex-066-bk', 'fw-778-yq', 'ex-252-bl', 'ez-285-bp', 'fp-866-sb', 'dj-074-fz',
                    'fp-505-sb', 'fp-949-sb', 'fc-256-tl', 'dp-575-rg', 'fp-940-sb', 'ez-441-ca', 'dm-599-bf', 'dx-894-ly',
                    'fw-920-xl', 'fc-210-tl', 'ez-390-bp', 'dx-775-ly', 'ez-505-br', 'fp-747-sb', 'gb-934-jt', 'el-304-ka',
                    'fp-719-sb', 'ez-352-jf', 'dm-213-by', 'ex-012-bk', 'dx-353-mb', 'df-108-nh', 'fp-714-sb', 'fw-843-yq',
                    'el-979-jz', 'fc-651-tl', 'fw-845-yq', 'dy-178-zg', 'dj-631-fz', 'dx-753-sy', 'el-055-ka', 'fw-848-yq',
                    'fc-717-tl', 'dx-841-ly', 'fp-729-sb', 'fw-817-yq', 'fw-053-xm', 'el-032-ka', 'ev-765-vw', 'fp-599-sb',
                    'fw-779-yq', 'fp-398-sb', 'fw-762-yq', 'dp-559-sc', 'fp-365-sb', 'ex-755-gf', 'dm-252-by', 'dp-539-sc',
                    'fp-495-sb', 'gb-837-jv', 'ez-777-bp', 'fw-793-yq', 'fp-896-sb', 'fw-049-xm', 'ez-179-br', 'ex-163-bl',
                    'dj-616-fz', 'ez-979-cj', 'gb-769-jt', 'fp-555-sb', 'ex-324-bl', 'dx-669-vl', 'ex-243-bl', 'fp-946-sb',
                    'dm-627-bf', 'fc-767-wg', 'gb-656-jt', 'fp-912-sb', 'ex-283-bl', 'fp-836-sb', 'ez-468-ca', 'ez-897-bp',
                    'fw-999-xl', 'fw-013-xm', 'fp-811-sb', 'fp-447-sb', 'ez-994-pt', 'ex-215-bk', 'dx-164-mb', 'fw-039-xm',
                    'ex-269-bl', 'fw-772-yq', 'gb-294-jv', 'fp-703-sb', 'fp-858-sb', 'fc-473-wg', 'ex-224-bl', 'el-006-ka',
                    'fw-031-xm', 'dx-235-mb', 'fw-768-yq', 'ez-356-br', 'fp-757-sb', 'dx-888-vl', 'ez-739-jf', 'fw-757-yq',
                    'fp-643-sb', 'fp-853-sb', 'fc-376-tl', 'fp-779-sb', 'fp-830-sb', 'ez-929-pt', 'fp-856-sb', 'fp-944-sb',
                    'fc-894-wg', 'fp-741-sb', 'ez-942-cj', 'dx-365-mb', 'fw-788-yq', 'eh-657-ka', 'fw-839-yq', 'dx-769-sy',
                    'ex-901-bp', 'fp-953-sb', 'ez-838-bp', 'ex-938-bp', 'fc-484-tl', 'ex-192-bk', 'dx-802-ly', 'el-012-ka',
                    'dx-159-mb', 'ew-644-ax', 'ex-146-bk', 'dx-331-mb', 'ex-921-bp', 'ez-322-br', 'fp-659-sb', 'fw-018-xm',
                    'dx-307-mb', 'el-317-ka', 'fw-834-yq', 'ez-587-bp', 'ex-104-bk', 'ez-006-ck', 'dp-634-rg', 'el-429-ka',
                    'fp-803-sb', 'dp-646-rg', 'el-045-ka', 'ez-806-bp', 'dm-211-by', 'dx-380-mb', 'fp-889-sb', 'fp-904-sb',
                    'fw-867-xl', 'ex-019-bq', 'fw-781-yq', 'ez-876-bp', 'df-135-sf', 'fp-626-sb', 'dx-358-mb', 'ez-739-bp',
                    'dm-168-by', 'ez-701-bp', 'dx-099-mb', 'fp-956-sb', 'ex-311-bl', 'fc-307-tl', 'ez-548-br', 'dj-560-fz',
                    'fp-880-sb', 'fp-347-sb', 'fp-821-sb', 'fw-906-xl', 'ex-072-bq', 'fp-634-sb', 'fw-996-xl', 'dm-661-bf',
                    'ex-300-bl', 'dm-311-by', 'fw-783-yq', 'dx-318-mb', 'dj-641-fz', 'df-108-nh', 'df-237-nh', 'dj-616-fz',
                    'df-146-nh', 'df-171-sf', 'df-169-yh', 'dj-395-fz', 'dj-074-fz', 'dj-658-fz', 'df-168-sf', 'dj-560-fz',
                    'df-135-sf', 'df-159-sf', 'dj-631-fz', 'dj-882-fy', 'dj-534-fz', 'dj-364-fz', 'dj-568-fz', 'dj-550-fz',
                    'dm-202-by', 'dp-590-sc', 'el-022-ka', 'dp-614-rm', 'dp-543-rm', 'dm-633-bf', 'dp-620-sc', 'eh-501-ka',
                    'eh-620-ka', 'dy-126-zg', 'eh-527-ka', 'fw-937-xl', 'fw-989-xl', 'fw-810-yq', 'fw-794-yq', 'fw-770-yq',
                    'fw-044-xm', 'fw-835-yq', 'fw-888-xl', 'fw-946-xl', 'fw-973-xl', 'fw-988-xl', 'fw-800-yq', 'fw-830-yq',
                    'dx-154-mb', 'dx-231-mb', 'dx-226-mb', 'dx-152-mb', 'dx-223-mb', 'dx-786-sy', 'el-450-ka', 'dx-112-mb',
                    'dx-343-mb', 'dx-244-mb', 'el-440-ka', 'dx-646-vl', 'dx-239-mb', 'el-419-ka', 'el-457-ka', 'el-436-ka',
                    'ex-991-bp', 'ex-040-bk', 'ex-243-bk', 'ex-045-bq', 'ex-100-bq', 'ex-151-bq', 'ex-462-bp', 'ex-474-bp',
                    'ex-489-bp', 'ex-958-bp', 'ex-974-bp', 'ex-181-bl', 'ex-202-bl', 'ex-340-bl', 'ez-387-br', 'ga-242-gl',
                    'ez-318-bp', 'ez-468-bp', 'ez-266-jf', 'ez-043-ck', 'ez-521-bp', 'ez-441-br', 'ez-627-bp', 'ez-412-jf',
                    'ez-253-br', 'ez-283-br', 'ez-402-ca', 'ez-491-bp', 'fp-907-sb', 'fc-783-wf', 'fp-482-sb', 'fp-431-sb',
                    'fp-894-sb', 'fp-933-sb', 'fp-883-sb', 'fp-419-sb', 'fp-668-sb', 'fp-929-sb', 'fp-572-sb', 'fp-827-sb',
                    'fp-463-sb', 'fp-615-sb', 'fp-814-sb', 'fp-843-sb', 'fp-900-sb', 'fp-588-sb', 'fp-918-sb', 'fc-570-wl',
                    'fc-717-tl', 'fc-894-wg', 'fc-376-tl', 'fc-288-wl', 'fc-397-tl', 'fc-981-wg', 'fc-693-wl', 'fc-808-wl',
                    'fc-210-tl', 'fc-767-wg', 'fc-326-wl', 'fc-227-xc', 'fc-256-tl', 'ew-644-ax', 'ev-765-vw', 'dp-377-bn',
                    'ev-765-vw', 'eh-567-ka', 'fp-873-sb', 'el-992-jz', 'df-098-yh', 'eh-638-ka', 'ez254bp', 'ex066bk',
                    'fw778yq', 'ex252bl', 'ez285bp', 'fp866sb', 'dj074fz', 'fp505sb', 'fp949sb', 'fc256tl', 'dp575rg',
                    'fp940sb', 'ez441ca', 'dm599bf', 'dx894ly', 'fw920xl', 'fc210tl', 'ez390bp', 'dx775ly', 'ez505br',
                    'fp747sb', 'gb934jt', 'el304ka', 'fp719sb', 'ez352jf', 'dm213by', 'ex012bk', 'dx353mb', 'df108nh',
                    'fp714sb', 'fw843yq', 'el979jz', 'fc651tl', 'fw845yq', 'dy178zg', 'dj631fz', 'dx753sy', 'el055ka',
                    'fw848yq', 'fc717tl', 'dx841ly', 'fp729sb', 'fw817yq', 'fw053xm', 'el032ka', 'ev765vw', 'fp599sb',
                    'fw779yq', 'fp398sb', 'fw762yq', 'dp559sc', 'fp365sb', 'ex755gf', 'dm252by', 'dp539sc', 'fp495sb',
                    'gb837jv', 'ez777bp', 'fw793yq', 'fp896sb', 'fw049xm', 'ez179br', 'ex163bl', 'dj616fz', 'ez979cj',
                    'gb769jt', 'fp555sb', 'ex324bl', 'dx669vl', 'ex243bl', 'fp946sb', 'dm627bf', 'fc767wg', 'gb656jt',
                    'fp912sb', 'ex283bl', 'fp836sb', 'ez468ca', 'ez897bp', 'fw999xl', 'fw013xm', 'fp811sb', 'fp447sb',
                    'ez994pt', 'ex215bk', 'dx164mb', 'fw039xm', 'ex269bl', 'fw772yq', 'gb294jv', 'fp703sb', 'fp858sb',
                    'fc473wg', 'ex224bl', 'el006ka', 'fw031xm', 'dx235mb', 'fw768yq', 'ez356br', 'fp757sb', 'dx888vl',
                    'ez739jf', 'fw757yq', 'fp643sb', 'fp853sb', 'fc376tl', 'fp779sb', 'fp830sb', 'ez929pt', 'fp856sb',
                    'fp944sb', 'fc894wg', 'fp741sb', 'ez942cj', 'dx365mb', 'fw788yq', 'eh657ka', 'fw839yq', 'dx769sy',
                    'ex901bp', 'fp953sb', 'ez838bp', 'ex938bp', 'fc484tl', 'ex192bk', 'dx802ly', 'el012ka', 'dx159mb',
                    'ew644ax', 'ex146bk', 'dx331mb', 'ex921bp', 'ez322br', 'fp659sb', 'fw018xm', 'dx307mb', 'el317ka',
                    'fw834yq', 'ez587bp', 'ex104bk', 'ez006ck', 'dp634rg', 'el429ka', 'fp803sb', 'dp646rg', 'el045ka',
                    'ez806bp', 'dm211by', 'dx380mb', 'fp889sb', 'fp904sb', 'fw867xl', 'ex019bq', 'fw781yq', 'ez876bp',
                    'df135sf', 'fp626sb', 'dx358mb', 'ez739bp', 'dm168by', 'ez701bp', 'dx099mb', 'fp956sb', 'ex311bl',
                    'fc307tl', 'ez548br', 'dj560fz', 'fp880sb', 'fp347sb', 'fp821sb', 'fw906xl', 'ex072bq', 'fp634sb',
                    'fw996xl', 'dm661bf', 'ex300bl', 'dm311by', 'fw783yq', 'dx318mb', 'dj641fz', 'df108nh', 'df237nh',
                    'dj616fz', 'df146nh', 'df171sf', 'df169yh', 'dj395fz', 'dj074fz', 'dj658fz', 'df168sf', 'dj560fz',
                    'df135sf', 'df159sf', 'dj631fz', 'dj882fy', 'dj534fz', 'dj364fz', 'dj568fz', 'dj550fz', 'dm202by',
                    'dp590sc', 'el022ka', 'dp614rm', 'dp543rm', 'dm633bf', 'dp620sc', 'eh501ka', 'eh620ka', 'dy126zg',
                    'eh527ka', 'fw937xl', 'fw989xl', 'fw810yq', 'fw794yq', 'fw770yq', 'fw044xm', 'fw835yq', 'fw888xl',
                    'fw946xl', 'fw973xl', 'fw988xl', 'fw800yq', 'fw830yq', 'dx154mb', 'dx231mb', 'dx226mb', 'dx152mb',
                    'dx223mb', 'dx786sy', 'el450ka', 'dx112mb', 'dx343mb', 'dx244mb', 'el440ka', 'dx646vl', 'dx239mb',
                    'el419ka', 'el457ka', 'el436ka', 'ex991bp', 'ex040bk', 'ex243bk', 'ex045bq', 'ex100bq', 'ex151bq',
                    'ex462bp', 'ex474bp', 'ex489bp', 'ex958bp', 'ex974bp', 'ex181bl', 'ex202bl', 'ex340bl', 'ez387br',
                    'ga242gl', 'ez318bp', 'ez468bp', 'ez266jf', 'ez043ck', 'ez521bp', 'ez441br', 'ez627bp', 'ez412jf',
                    'ez253br', 'ez283br', 'ez402ca', 'ez491bp', 'fp907sb', 'fc783wf', 'fp482sb', 'fp431sb', 'fp894sb',
                    'fp933sb', 'fp883sb', 'fp419sb', 'fp668sb', 'fp929sb', 'fp572sb', 'fp827sb', 'fp463sb', 'fp615sb',
                    'fp814sb', 'fp843sb', 'fp900sb', 'fp588sb', 'fp918sb', 'fc570wl', 'fc717tl', 'fc894wg', 'fc376tl',
                    'fc288wl', 'fc397tl', 'fc981wg', 'fc693wl', 'fc808wl', 'fc210tl', 'fc767wg', 'fc326wl', 'fc227xc',
                    'fc256tl', 'ew644ax', 'ev765vw', 'dp377bn', 'ev765vw', 'eh567ka', 'fp873sb', 'el992jz', 'df098yh', 'eh638ka','el032xa']

    car_info = get_car_info(message)
    if car_info:
        if message in radar_priver:
            return f"Voiture Radar Confirmée!!!\n{car_info}"
        else:
            return f"Cette voiture ne semble pas être un radar\n{car_info}"
    if not car_info:
        return f"Désolé, nous ne parvenons pas à trouver les informations de cette plaque d'immatriculation."

def handle_message(update, context):
    text = str(update.message.text).lower()
    logging.info(f'User ({update.message.chat.id}) says: {text}')

    # Bot response
    response = get_response(text)
    update.message.reply_text(response)


def error(update, context):
    # Logs errors
    logging.error(f'Update {update} caused error {context.error}')


# Run the programme
if __name__ == '__main__':
    updater = Updater(API_KEY, use_context=True)
    dp = updater.dispatcher

    # Messages
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # Log all errors
    dp.add_error_handler(error)

    # Run the bot
    updater.start_polling(poll_interval=1.0)
    updater.idle()
