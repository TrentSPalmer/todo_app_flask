## tables in your postgresql todo database
<table border="1">
<caption>List of relations</caption>
<tr>
<th align="center">Schema</th>
<th align="center">Name</th>
<th align="center">Type</th>
<th align="center">Owner</th>
</tr>
<tr valign="top">
<td align="left">public</td>
<td align="left">category</td>
<td align="left">table</td>
<td align="left">todo</td>
</tr>
<tr valign="top">
<td align="left">public</td>
<td align="left">category_id_seq</td>
<td align="left">sequence</td>
<td align="left">todo</td>
</tr>
<tr valign="top">
<td align="left">public</td>
<td align="left">contributor</td>
<td align="left">table</td>
<td align="left">todo</td>
</tr>
<tr valign="top">
<td align="left">public</td>
<td align="left">contributor_id_seq</td>
<td align="left">sequence</td>
<td align="left">todo</td>
</tr>
<tr valign="top">
<td align="left">public</td>
<td align="left">email_white_list</td>
<td align="left">table</td>
<td align="left">todo</td>
</tr>
<tr valign="top">
<td align="left">public</td>
<td align="left">email_white_list_id_seq</td>
<td align="left">sequence</td>
<td align="left">todo</td>
</tr>
<tr valign="top">
<td align="left">public</td>
<td align="left">task</td>
<td align="left">table</td>
<td align="left">todo</td>
</tr>
<tr valign="top">
<td align="left">public</td>
<td align="left">task_id_seq</td>
<td align="left">sequence</td>
<td align="left">todo</td>
</tr>
</table>
<p>(8 rows)<br />
</p>

### email_white_list

<table border="1">
<caption>Table &quot;public.email_white_list&quot;</caption>
<tr>
<th align="center">Column</th>
<th align="center">Type</th>
<th align="center">Collation</th>
<th align="center">Nullable</th>
<th align="center">Default</th>
</tr>
<tr valign="top">
<td align="left">id</td>
<td align="left">integer</td>
<td align="left">&nbsp; </td>
<td align="left">not null</td>
<td align="left">nextval('email_white_list_id_seq'::regclass)</td>
</tr>
<tr valign="top">
<td align="left">email</td>
<td align="left">character varying(120)</td>
<td align="left">&nbsp; </td>
<td align="left">not null</td>
<td align="left">&nbsp; </td>
</tr>
</table>
<p>Indexes:<br />
&nbsp;&nbsp;&nbsp;&nbsp;&quot;email_white_list_pkey&quot; PRIMARY KEY, btree (id)<br />
&nbsp;&nbsp;&nbsp;&nbsp;&quot;email_white_list_email_key&quot; UNIQUE CONSTRAINT, btree (email)<br />
</p>

### contributor

<table border="1">
<caption>Table &quot;public.contributor&quot;</caption>
<tr>
<th align="center">Column</th>
<th align="center">Type</th>
<th align="center">Collation</th>
<th align="center">Nullable</th>
<th align="center">Default</th>
</tr>
<tr valign="top">
<td align="left">id</td>
<td align="left">integer</td>
<td align="left">&nbsp; </td>
<td align="left">not null</td>
<td align="left">nextval('contributor_id_seq'::regclass)</td>
</tr>
<tr valign="top">
<td align="left">name</td>
<td align="left">character varying(64)</td>
<td align="left">&nbsp; </td>
<td align="left">not null</td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">email</td>
<td align="left">character varying(120)</td>
<td align="left">&nbsp; </td>
<td align="left">not null</td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">password_hash</td>
<td align="left">character varying(128)</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">totp_key</td>
<td align="left">character(16)</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">use_totp</td>
<td align="left">boolean</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">false</td>
</tr>
</table>
<p>Indexes:<br />
&nbsp;&nbsp;&nbsp;&nbsp;&quot;contributor_pkey&quot; PRIMARY KEY, btree (id)<br />
&nbsp;&nbsp;&nbsp;&nbsp;&quot;contributor_email_key&quot; UNIQUE CONSTRAINT, btree (email)<br />
&nbsp;&nbsp;&nbsp;&nbsp;&quot;contributor_name_key&quot; UNIQUE CONSTRAINT, btree (name)<br />
</p>

### category

<table border="1">
<caption>Table &quot;public.category&quot;</caption>
<tr>
<th align="center">Column</th>
<th align="center">Type</th>
<th align="center">Collation</th>
<th align="center">Nullable</th>
<th align="center">Default</th>
</tr>
<tr valign="top">
<td align="left">id</td>
<td align="left">integer</td>
<td align="left">&nbsp; </td>
<td align="left">not null</td>
<td align="left">nextval('category_id_seq'::regclass)</td>
</tr>
<tr valign="top">
<td align="left">name</td>
<td align="left">character varying(128)</td>
<td align="left">&nbsp; </td>
<td align="left">not null</td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">contributor_id</td>
<td align="left">integer</td>
<td align="left">&nbsp; </td>
<td align="left">not null</td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">hidden</td>
<td align="left">boolean</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">false</td>
</tr>
</table>
<p>Indexes:<br />
&nbsp;&nbsp;&nbsp;&nbsp;&quot;category_pkey&quot; PRIMARY KEY, btree (id)<br />
&nbsp;&nbsp;&nbsp;&nbsp;&quot;category_name_key&quot; UNIQUE CONSTRAINT, btree (name)<br />
</p>

### task

<table border="1">
<caption>Table &quot;public.task&quot;</caption>
<tr>
<th align="center">Column</th>
<th align="center">Type</th>
<th align="center">Collation</th>
<th align="center">Nullable</th>
<th align="center">Default</th>
</tr>
<tr valign="top">
<td align="left">id</td>
<td align="left">integer</td>
<td align="left">&nbsp; </td>
<td align="left">not null</td>
<td align="left">nextval('task_id_seq'::regclass)</td>
</tr>
<tr valign="top">
<td align="left">content</td>
<td align="left">text</td>
<td align="left">&nbsp; </td>
<td align="left">not null</td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">contributor_id</td>
<td align="left">integer</td>
<td align="left">&nbsp; </td>
<td align="left">not null</td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">catid</td>
<td align="left">integer</td>
<td align="left">&nbsp; </td>
<td align="left">not null</td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">done</td>
<td align="left">boolean</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">false</td>
</tr>
<tr valign="top">
<td align="left">priority</td>
<td align="left">integer</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
</tr>
<tr valign="top">
<td align="left">timestamp</td>
<td align="left">timestamp without time zone</td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
<td align="left">&nbsp; </td>
</tr>
</table>
<p>Indexes:<br />
&nbsp;&nbsp;&nbsp;&nbsp;&quot;task_pkey&quot; PRIMARY KEY, btree (id)<br />
</p>

