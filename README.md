## Another small project that I did as part of the recruitment stage.

### This time website is more than just api,because first time I used bootstrap to make it actually look good compared to my last projects.

### REST API DOCUMENTATION

You can actually use query params to filter objects. After rest url (https://api-library-app.herokuapp.com/books/api/) You have to specify <strong>? character</strong> and then params of your choice. You can obviously mix it up but after every single param you have to put <strong>& character</strong>.

#### Example:

https://api-library-app.herokuapp.com/books/api/?search=hobbit

### Params list:
<li><strong>search</strong> - used to query any word in title, author name and language</li>
<li><strong>title</strong> - used to search any word that any title will contain
<li><strong>pub_date_after</strong> - minimal range of date. You have to provide actual date here like <strong>pub_date_after=2010-01-01</strong>
<li><strong>pub_date_before</strong> - maximum range of date. You can mix it up with minimal range param
<li><strong>author</strong> - used to look for word that author name contains. 
<li><strong>authors</strong> - used to look for direct authors. Important thing is that You have to put <strong>+ character</strong> instead of spaces. You can look for more than just one author. To do this, You have to put <strong>& character</strong> and then specify authors param again like that: <strong>authors=John+Ronald+Reuel+Tolkien&authors=J.+R.+R.+Tolkien</strong>
<li><strong>languages</strong> - used to look for languages. It can be also used more than once.

## Live site:

https://api-library-app.herokuapp.com/