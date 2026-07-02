import {
    Box,
    Button,
    Checkbox,
    Container,
    FormControlLabel,
    IconButton,
    InputAdornment,
    Paper,
    TextField,
    Typography
} from "@mui/material";

import {
    Visibility,
    VisibilityOff
} from "@mui/icons-material";

import { useState } from "react";

export default function Login() {

    const [showPassword,setShowPassword]=useState(false);

    return(

        <Container maxWidth="sm">

            <Box
                display="flex"
                justifyContent="center"
                alignItems="center"
                minHeight="100vh"
            >

                <Paper
                    elevation={8}
                    sx={{
                        p:5,
                        width:"100%",
                        borderRadius:4
                    }}
                >

                    <Typography
                        variant="h4"
                        fontWeight="bold"
                        color="primary"
                        textAlign="center"
                        mb={1}
                    >

                        GIS Survey

                    </Typography>

                    <Typography
                        color="text.secondary"
                        textAlign="center"
                        mb={4}
                    >

                        Property Survey Application

                    </Typography>

                    <TextField

                        fullWidth

                        label="Mobile Number"

                        margin="normal"

                    />

                    <TextField

                        fullWidth

                        label="Password"

                        margin="normal"

                        type={showPassword ? "text":"password"}

                        InputProps={{

                            endAdornment:

                                <InputAdornment position="end">

                                    <IconButton

                                        onClick={()=>setShowPassword(!showPassword)}

                                    >

                                        {

                                            showPassword ?

                                            <VisibilityOff/>

                                            :

                                            <Visibility/>

                                        }

                                    </IconButton>

                                </InputAdornment>

                        }}

                    />

                    <FormControlLabel

                        control={<Checkbox/>}

                        label="Remember Me"

                        sx={{mt:1}}

                    />

                    <Button

                        variant="contained"

                        fullWidth

                        size="large"

                        sx={{

                            mt:3,

                            borderRadius:3,

                            height:50

                        }}

                    >

                        LOGIN

                    </Button>

                </Paper>

            </Box>

        </Container>

    )

}