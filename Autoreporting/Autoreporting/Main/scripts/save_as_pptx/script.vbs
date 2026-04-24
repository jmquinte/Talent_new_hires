' VISUAL BASIC SCRIPT - GENERATES PPTX based on XML file '
' EXEC CSCRIPT.EXE C:\...\script.vbs "C:\..." '

' FUNCTION Generate Presentation '
'   RETURNS - pointer to PowerPoint Presentation '
Private Function generate_presentation( )
    ' Vars '
    Dim ppA, ppP
    Dim path, fso
    ' Get script.vbs path '
    Set fso = CreateObject( "Scripting.FileSystemObject" )
    path = fso.GetParentFolderName( WScript.ScriptFullName )
    ' Create Presentation '
    Set ppA = CreateObject( "PowerPoint.Application" ) 
    Set ppP = ppA.Presentations.Add
    ' Read POTX template '
    On Error Resume Next
        ppP.ApplyTemplate( path & "\template.potx" )
    ppA.Visible = True
    ' RETURN '
    Set generate_presentation = ppP
End Function

' SUB Add Slide Title '
Private Sub add_slideTitle( ByVal xml, ByRef ppP )
    ' Vars '
    Dim ppS
    Dim title, subtitle
    ' Add Slide - Style 1, Index 1 '
    Set ppS = ppP.Slides.Add( 1, 1 )
    ' Get data from XML '
    title = xml.selectSingleNode( "./SLIDETITLE/TITLE/ITEM" ).text
    subtitle = xml.selectSingleNode( "./SLIDETITLE/SUBTITLE/ITEM" ).text
    ' Set data to PPTX '
    ppS.Shapes( 1 ).TextFrame.TextRange.Text = title
    ppS.Shapes( 2 ).TextFrame.TextRange.Text = subtitle
End Sub

' SUB Add Slide '
Private Sub add_slide( ByVal  xml, ByRef ppP, ByVal path )
    ' Vars '
    Dim ppS
    Dim title, description, image, slides, slide, n
    ' Select all SLIDE objects in XML '
    Set slides = xml.SelectNodes( "./SLIDE" )
    n = 2
    ' Iterate '
    For Each slide in slides
        ' Add Slide - Style 2 '
        Set ppS = ppP.Slides.Add( n, 2 )
        ' Get data from XML '
        title = slide.selectSingleNode( "./TITLE/ITEM" ).text
        description = slide.selectSingleNode( "./DESCRIPTION/ITEM" ).text
        image = slide.selectSingleNode( "./IMAGE/ITEM" ).text
        ' Set title '
        ppS.Shapes( 1 ).TextFrame.TextRange.Text = title
        ' Set text and resize shape '
        With ppS.Shapes( 2 )
            .TextFrame.TextRange.Text = description
            .Width = 300
        End With
        ' Add Rectangle and fill with image ' 
        ppS.Shapes.AddShape 1, 400, 100, 500, 400 
        ppS.Shapes(3).Fill.UserPicture path & image
        n = n + 1
    Next
End Sub

' FUNCTION Read file '
'   RETURN - xml nodes ojbect '
Private Function read_file( ByVal file )
    ' Vars '
    Dim xmlDoc
    Dim Presentation
    ' XML Parser ' 
    Set xmlDoc = CreateObject("Msxml2.DOMDocument")
    xmlDoc.load( file )
    ' Return '
    Set read_file = xmlDoc.selectSingleNode( "/PRESENTATION" )
End Function

' SUB Engine '
Private Sub engine( ByVal path )
    ' Vars '
    Dim xml, presentation, slideTitle, slides
    Dim title, subtitle
    ' Create Presentation '
    Set presentation = generate_presentation()
    Set xml = read_file( path & "test.xml" )
    Call add_slideTitle( xml, presentation )
    Call add_slide( xml, presentation, path )
    Call presentation.SaveAs( path & "Results" )
End Sub

' MAIN '
Private Sub main()
    Dim path
    path = WScript.Arguments( 0 )
    Call engine( path )
End Sub

main()
